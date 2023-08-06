.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="Grid-Header" src="https://github.com/akbar-amin/resources/blob/master/grid-header.gif">
        </a>
    </p>
    <p align="center">
        <a href="https://pypi.python.org/pypi/disctext"><img alt="Pypi version" src="https://img.shields.io/pypi/v/disctext.svg"></a>
        <a href="https://github.com/akbar-amin/disctext/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
    </p>
  
********
Disctext
********

``disctext`` utilizes ``cv2`` and ``numpy`` to read and convert video frames into text frames. The resulting frames can be packed into Markdown `code blocks <https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51#code-blocks>`_ and shared on Discord, or simply be viewed in console like a video.

Code blocks are used to escape Discord's auto-formatting, which would otherwise ruin most ASCII art since the glyphs would get mixed up with format characters.
However, code blocks also provide contrast and can add "color" to text via syntax highlights.

.. end-intro

Installation
------------

::

    pip install disctext==1.0.0

For discord interaction, a bot token is required with permissions to send messages. 
Make sure to also have "Developer Mode" enabled in user settings to retrieve channel ids.


Features
--------------

Art customization settings are stored in `disctext.Canvas`:


- font (str): Name of character mapping set to use when creating art. Defaults to "basic".
    - Font names and their respective sets can be found in ``disctext.fonts``.
- syntax (str): Language identifier to use for syntax highlighting. Defaults to an empty string.
    - Most, if not all, languages can be found in ``disctext.syntax``. However, you can pass in a string identifier yourself.
- invert (bool): Reverse the character set mappings from DARK -> LIGHT to LIGHT -> DARK. Defaults to False.
    - This setting will have a noticeable difference when using the following fonts: ``basic``, ``detail``, ``braille1``, ``braille2``
- minCols, maxCols (int): Lower and upper width bounds. Defaults to 40 and 100, respectively.
    - The value maximizing the frame's area is used.  
- minArea (int): Lower area bound. Defaults to 0, or pass-through.
    - After packing a frame, if the area of the frame *without* white spaces is less than this value, the frame is skipped.
- maxArea (int): Upper area bound. Defaults to 1985 [#]_.
    - After packing a frame, if the total area of the frame is greater than this value, the frame is skipped.


Other features:

- Set the total number of frames to read. Refer to ``disctext.Client.add_canvas`` and ``disctext.Monitor.display``. Default to all frames.
- Adjust the Discord message interval via the attribute ``disctext.Client.RATELIMIT``. Defaults to 0.8 [#]_.
- An animated progress bar is shown when using with Discord; displaying the current and total frame count, as well as an ETA in minutes.
- Extension of ``discord.Client`` for convenience. Refer to `Usage` and this example.

TODO:

- Allow setting a range of frames via "start" and "stop" parameters
- Check for the "opposite" white space character when inverted.

Usage
-----

To display on Discord, specify a video file along with a bot token and destination channel.

.. code-block:: python

    import disctext

    video = disctext.Video("PATH")

    # create a canvas with default settings
    canvas = disctext.Canvas()
    client = disctext.Client(video)

    # run the configuration in the desired channel
    client.add_canvas(canvas, 842291894464675850)
    client.run("TOKEN")


To avoid managing id's, ``disctext`` extends ``discord.Client`` to allow searching for guilds and channels by name and/or auto-creating text channels.

.. code-block:: python

    import disctext

    video = disctext.Video("PATH")
    canvas1 = disctext.Canvas(font="basic")
    canvas2 = disctext.Canvas(font="detail")
    client = disctext.Client(video)

    # "DemoChannel" will be created in "DemoGuild" if it does not exist
    client.add_canvas(canvas1, "DemoChannel")

    # A channel will be created in "DemoGuild" based on the video title 
    client.add_canvas(canvas2)
    
    client.run("TOKEN", "DemoGuild")


You can view the art in console using a similar procedure. Frames are not packed into code blocks in this case.

.. code-block:: python

    import disctext

    video = disctext.Video("PATH")

    # "syntax" will have no effect since the frames are not packed
    canvas = disctext.Canvas(font="braille1", minCols=60, maxCols=70)

    # show the first 500 frames at 60 FPS
    monitor = disctext.Monitor(video, rate=60)
    monitor.display(canvas, 500)

    
More examples can be found here.

Playback (Discord) 
------------------

1. Using the Discord search bar, search for the ``NOW PLAYING:`` message sent by the bot at startup.
2. Find and click on a search result; newest results will appear first.
3. Click anywhere inside the cell and hold the down arrow key.

    3a. Resize the Discord app/webpage to fit the frames more nicely.

The playback "speed" is around 30 FPS, or messages-per-second. 

It's worth noting that Discord loads messages as HTTP requests in chunks of 50, so there is a short (~120-200 ms) pause every other second-or-so. 
The pauses are most likely due to server response times, content download speed, etc. 
Knowing this, one can take advantage of request caching and run the playback twice, where the second playback will noticeably run smoother.


Demo
----

Aside from the original clips [#]_ [#]_, all recordings were done on Discord using the method above. Demos can be found in `this <https://discord.gg/jhvBB3n5Pc>`_ server as well. 


.. raw:: html

    <p align="center">
        <a href="#demo">
            <img alt="Grid-Demo" src="https://github.com/akbar-amin/resources/blob/master/grid.gif">
        </a>
    </p>
    
    
.. |grid1| image:: https://github.com/akbar-amin/resources/blob/master/grid-1.gif
.. |grid2| image:: https://github.com/akbar-amin/resources/blob/master/grid-2.gif
.. |grid3| image:: https://github.com/akbar-amin/resources/blob/master/grid-3.gif
.. |grid4| image:: https://github.com/akbar-amin/resources/blob/master/grid-4.gif
.. |grid5| image:: https://github.com/akbar-amin/resources/blob/master/grid-5.gif
.. |grid6| image:: https://github.com/akbar-amin/resources/blob/master/grid-6.gif
.. |grid7| image:: https://github.com/akbar-amin/resources/blob/master/grid-7.gif
.. |grid8| image:: https://github.com/akbar-amin/resources/blob/master/grid-8.gif
.. |grid9| image:: https://github.com/akbar-amin/resources/blob/master/grid-9.gif
.. |steamboat1| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-1.gif
.. |steamboat2| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-2.gif
.. |steamboat3| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-3.gif
.. |steamboat4| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-4.gif
.. |steamboat5| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-5.gif
.. |steamboat6| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-6.gif
.. |steamboat7| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-7.gif
.. |steamboat8| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-8.gif
.. |steamboat9| image:: https://github.com/akbar-amin/resources/blob/master/steamboat-9.gif
    

.. table::
    :align: center 
    :widths: grid

    
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+
    | |grid1|                                 | |grid2|                                 | |grid3|                                 |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+
    | |grid4|                                 | |grid5|                                 | |grid6|                                 |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+
    | |grid7|                                 | |grid8|                                 | |grid9|                                 |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+


.. raw:: html

    <p align="center">
        <a href="#demo">
            <img alt="Steamboat-Demo" src="https://github.com/akbar-amin/resources/blob/master/steamboat.gif">
        </a>
    </p>





.. table::
    :align: center 
    :widths: grid

    +-----------------------------------------+-----------------------------------------+-----------------------------------------+
    | |steamboat1|                            | |steamboat2|                            | |steamboat3|                            |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+
    | |steamboat4|                            | |steamboat5|                            | |steamboat6|                            |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+
    | |steamboat7|                            | |steamboat8|                            | |steamboat9|                            |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    |                                         |                                         |                                         |
    +-----------------------------------------+-----------------------------------------+-----------------------------------------+



.. [#] If using with Discord, this value should not go above default since the max character limit is 2000 and some space must be allocated for packing.

.. [#] This value should not go below the default unless you wish to experience Discord rate limits. 

.. [#] *Grid [Psychedelic Animation]*. (2013, January 2). [Video]. `Youtube <https://www.youtube.com/watch?v=OWa5rzEOumQ>`_.

.. [#] *"Steamboat Willie"* Internet Archive, Walt Disney Animation Studios, 8 Nov. 1928, archive.org/details/SteamboatWillie. 
