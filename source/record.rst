Recording Events
================

Freeseer's primary use case is recording large events such as conferences.
You can run Freeseer locally and have the presenter record their desktop,
but a much more useful configuration is when Freeseer is used from a dedicated
laptop to record VGA output from the presenter's laptop.

Equipment Needed
-------------
* A working installation of Freeseer on a dedicated computer for recording
* VGA Capture Device

  * We recommend an `Epiphan frame grabber <http://www.epiphan.com/products/frame-grabbers/>`_
  * We use the `VGA2USB device <http://www.epiphan.com/products/frame-grabbers/vga2usb/>`_ (the red one)
    as it's the cheapest and does a decent job
* Wireless Microphones
  * We use Sennheiser EW100 G2

Setup
-----

.. raw:: html

  <iframe width="840" height="480" src="http://www.youtube-nocookie.com/embed/jXs8beuvvrM" frameborder="0" allowfullscreen></iframe>

Preparation
-----------
* Use the Talk Editor tool to enter all the talks and their info beforehand.
* Have the speakers disable their screen saver and power saving mode. [1]_

  * Linux users can use the caffeine app::

      sudo add-apt-repository ppa:caffeine-developers/ppa
      sudo apt-get update
      sudo apt-get install caffeine

Hosting the Videos
------------------
The Free and Open Source Software Learning Centre (FOSSLC) can place your videos
on `fosslc.org <http://fosslc.org>`_ for free if the talks are open source related.
FOSSLC will promote them on the site and host them on YouTube.
The site is somewhat popular and gets quite a few hits from various communities.
If you decide to use the services of FOSSLC, please email fosslc@gmail.com.
Of course you can always use your own hosting solution.

.. todo:: when a new laptop is plugged (eg when speakers are changing between talks).
          The first time you press record sometimes vga2usb sends you a jumbled signal.
          Strangely stopping and starting the recording fixes it.
          Like the resolution is off or you don't see any useful signal just noise.
          I think restarting the recording forces it to redetect the resolution properly.

.. rubric:: Footnotes

.. [1] If the presenter's laptop goes into power saving mode, then the vga2usb
       device loses the signal and you will have to pause and restart the recording.
