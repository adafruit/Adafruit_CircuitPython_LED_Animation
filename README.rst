Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-led_animation/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/led_animation/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/actions
    :alt: Build Status

A library to easily generate LED animations


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-led_animation/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-led-animation

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-led-animation

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-led-animation

Usage Example
=============

.. code-block:: python

    from adafruit_led_animation.animation import Comet, AnimationSequence, Chase
    from adafruit_led_animation.color import PURPLE, WHITE
    import neopixel
    import board

    pixels = neopixel.NeoPixel(board.D6, 32, brightness=0.2, auto_write=False)
    comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
    chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
    animations = AnimationSequence(comet, chase, advance_interval=15)

    while True:
        animations.animate()

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
