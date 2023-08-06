from __future__ import annotations

import os
import cv2
import asyncio
import itertools
import numpy as np
from dataclasses import dataclass

from .fonts import FONTMAP
from .const import BAR, TICK, STEPS, BLOCK, DONE, ESCAPE


@dataclass
class Canvas:
    font: str = "basic"
    syntax: str = ""
    invert: bool = False
    minCols: int = 40
    maxCols: int = 100
    minArea: int = 0
    maxArea: int = 1985

    def pack(self, text):
        return "".join([BLOCK, self.syntax, text, "\n", BLOCK])

    def valid(self, frame):
        return (len(frame) - frame.count(" ") >= self.minArea) \
            and len(frame) <= self.maxArea

    def chars(self):
        values = list(FONTMAP[self.font])
        return values[::-1] if self.invert else values[:]

    def maximize(self, ih, iw):
        sh = np.zeros(4)
        for tc in range(self.minCols, self.maxCols):
            tw = iw/tc
            th = tw * 2
            tr = ih/th
            ta = tr * tc
            if ta >= self.maxArea:
                break
            sh = np.array([th, tw, tr, tc], "i")
        return sh

    def __repr__(self):
        attrs = [("font", self.font),
                 ("syntax", self.syntax or None),
                 ("invert", self.invert)]
        return "<%s %s>" % (self.__class__.__name__, " ".join("%s=%s" % t for t in attrs))


class Monitor:

    TEMPLATE = "{} {}: {:3d}% {} {}/{} [ETA: {:.2f} min]"

    def __init__(self, video: Video, rate: float = 0.8):
        self.loop = asyncio.get_event_loop()
        self.video = video
        self.rate = rate
        self.task = None
        self.reset()

    def show(self, escape, text, flush=False):
        print(escape + text, flush=flush, end="")

    def progression(self):
        total, count = self.total, self.count
        status = next(self.steps) if count != total else DONE
        mins = max(0, (total - count) * self.rate * 1/60)
        ratio = count/max(1, total)
        width = int(50 * ratio)
        block = BAR + (TICK * width).ljust(50) + BAR
        bars = Monitor.TEMPLATE.format(
            status, self.video.name(), int(ratio * 100), block, count, total, mins)
        self.show("\r", bars)

    async def progressTask(self):
        while self.video.opened():
            spot = self.video.get(Video.POSITION)
            if spot > self.count:
                self.count = spot
                await self.loop.run_in_executor(
                    None, self.progression)
                if spot >= self.total:
                    break
            else:
                await asyncio.sleep(0)
        self.show("\r", "", True)
        self.reset()

    async def displayTask(self, canvas):
        count = 0
        height = None
        async for frame in self.video.draw(canvas, False):
            count += 1
            if height is None:
                height = frame.count("\n")
                self.show("", "\n" * height)
            self.show(ESCAPE * height, frame, True)
            if count == self.total:
                break
            await asyncio.sleep(1/self.rate)
        self.reset()

    def progress(self, total: int = None):
        self.video.open()
        self.total = total or self.video.get(Video.TOTAL)
        self.task = asyncio.ensure_future(self.progressTask())

    def display(self, canvas: Canvas, total: int = None):
        self.video.open()
        self.total = total or self.video.get(Video.TOTAL)
        self.task = asyncio.ensure_future(self.displayTask(canvas))
        try:
            self.loop.run_until_complete(self.task)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        self.reset()

    def reset(self):
        if self.video.opened():
            self.video.close()
        if self.task:
            self.task.cancel()
        self.task = None
        self.total = -1
        self.count = 0
        self.steps = itertools.cycle(STEPS)


class Video:

    TOTAL = cv2.CAP_PROP_FRAME_COUNT
    WIDTH = cv2.CAP_PROP_FRAME_WIDTH
    HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
    POSITION = cv2.CAP_PROP_POS_FRAMES

    def __init__(self, path: str):
        self.path = str(path)
        self.lock = asyncio.Lock()
        self.source = None

    def name(self):
        return os.path.split(self.path)[-1]

    def get(self, prop):
        return int(self.source.get(prop))

    def set(self, prop, value):
        self.source.set(prop, value)

    def open(self):
        if self.opened():
            raise ValueError("Video is already opened")
        self.source = cv2.VideoCapture(self.path)
        self.set(Video.POSITION, 0)

    def opened(self):
        return self.source is not None and self.source.isOpened()

    async def read(self):
        loop = asyncio.get_running_loop()
        while self.opened():
            success, image = await loop.run_in_executor(
                None, self.source.read)
            if not success:
                break
            yield cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    async def draw(self, canvas, pack: bool = True):
        async with self.lock:
            ch = canvas.chars()
            iw = self.get(Video.WIDTH)
            ih = self.get(Video.HEIGHT)
            h, w, r, c = canvas.maximize(ih, iw)
            async for im in self.read():
                text = ""
                for i, k in np.ndindex(r, c):
                    if k == 0:
                        text += "\n"
                    ROI = im[i*h:min((i+1)*h, ih), k*w:min((k+1)*w, iw)]
                    char = ch[int(min(ROI.mean()*len(ch)/255, len(ch)-1))]
                    text += char
                if pack:
                    text = canvas.pack(text)
                if canvas.valid(text):
                    yield text

    def close(self):
        if not self.opened():
            return
        self.source.release()
        self.source = None
        cv2.destroyAllWindows()

    def __del__(self):
        self.close()

    def __str__(self):
        return self.name()

    def __repr__(self):
        attrs = [
            ("name", self.name()),
            ("open", self.opened())]
        return "<%s %s>" % (self.__class__.__name__, " ".join("%s=%r" % t for t in attrs))
