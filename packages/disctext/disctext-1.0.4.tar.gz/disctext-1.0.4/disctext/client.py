import discord
import asyncio
import collections
from typing import Union, Optional

from .video import Video, Canvas, Monitor
from .const import NOTE, INFO, ERROR

class Client(discord.Client):

    RATELIMIT = 0.8

    def __init__(self, video: Video, **kwargs):
        super().__init__(**kwargs)
        self.video = video
        self.guild = None
        self.queue = collections.deque()

    def add_canvas(self, canvas: Canvas, channel: Optional[Union[str, int]] = None, count: Optional[int] = None):
        """ 
        Args:
            canvas: A customized ``Canvas`` object.
            channel: Discord channel id or name. Passing a name requires
                a guild id to be specified in ``run``. The channel is first 
                searched for and then created if it does not exist.
                By default, then the video's filename is used.
            count: Limit number of frames to read.
        """
        self.queue.append((canvas, channel, count))

    def add_sample(self, count: int, attrib: str, values: list, channel: Optional[Union[str, int]] = None, **kwargs):
        """
        Args:
            count: Same argument passed into ``add_canvas``.
            attrib: The ``Canvas`` attribute for which values will set.
            values: Sequence of values for the specified attribute.
                Canvases are created and queued in the same order.
            channel: Same argument passed into ``add_canvas``.  
        
        Keyword aguments are passed every ``Canvas`` created.
        """
        for value in values:
            canvas = Canvas(**kwargs)
            setattr(canvas, attrib, value)
            self.add_canvas(canvas=canvas, channel=channel, count=count)

    async def play(self):
        print(INFO, "Guild: %r" % self.guild or "<NoValue>")
        print(INFO, "Video: %r" % self.video)
        m = Monitor(self.video, self.RATELIMIT)
        while self.queue:
            canvas, channel, count = self.queue.popleft()
            try:
                target = await self._fetch(channel)
                print(INFO, "Target: %r" % target)
                print(INFO, "Canvas: %r" % canvas)
                m.progress(count)
                await target.send(
                    canvas.pack('\nNOW PLAYING: "%s" %r' % (self.video, canvas)))
                async for frame in self.video.draw(canvas):
                    await target.send(frame)
                    await asyncio.sleep(self.RATELIMIT)
            except Exception as e:
                print("\r")
                print(ERROR, "Error: %s" % e)
            finally:
                m.reset()
        await self.close()

    async def _fetch(self, channel):
        chann = str(channel) if channel else self.video.name().split(".")[0]
        value = None
        if chann.isdigit():
            value = await self.fetch_channel(int(channel))
        else:
            for ch in self.guild.channels:
                if chann == ch.name:
                    value = ch
        if value is None:
            value = await self.guild.create_text_channel(str(channel))
        return value

    async def _startup(self, guild):
        await self._ready.wait()
        print(NOTE, "Connected")
        if not self.queue:
            raise ValueError("At least one canvas must be set")
        if guild:
            if str(guild).isdigit():
                self.guild = await self.fetch_guild(int(guild))
            else:
                for g in self.guilds:
                    if g.name == guild:
                        self.guild = g

    async def close(self):
        self.video.close()
        await super().close()

    def run(self, token: str, guild: Optional[Union[str, int]] = None):
        """ 
        Args:
            token: Discord bot token 
            guild: Discord guild id or name. Used for auto-creating
                text channels and/or searching for channels by name.
        """
        self.loop.create_task(self.start(token))
        try:
            self.loop.run_until_complete(self._startup(guild))
            self.loop.run_until_complete(self.play())
        except KeyboardInterrupt:
            print("\r")
            print(NOTE, "Exiting...")
            self.loop.run_until_complete(self.close())        
        print(NOTE, "Disconnected")


