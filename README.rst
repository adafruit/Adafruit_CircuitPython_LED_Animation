Introduction
============

.. image:: https://readthedocs.org/projects/adafruit_circuitpython_led_animation/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/led-animation/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/actions
    :alt: Build Status

Perform a variety of LED animation tasks

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.


Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-led-animation/>`_. To install for current user:

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

    import board
    import neopixel
    from adafruit_led_animation.animation.blink import Blink
    import adafruit_led_animation.color as color

    # Works on Circuit Playground Express and Bluefruit.
    # For other boards, change board.NEOPIXEL to match the pin to which the NeoPixels are attached.
    pixel_pin = board.NEOPIXEL
    # Change to match the number of pixels you have attached to your board.
    num_pixels = 10

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels)
    blink = Blink(pixels, 0.5, color.PURPLE)

    while True:
        blink.animate()

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/led-animation/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/apatt/CircuitPython_LED_Animation/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Zip release files
-----------------

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix circuitpython-led_animation --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
