Recording Events
================

.. todo:: embed youtube video where Andrew shows setup

Freeseer's primary use case is recording large events such as conferences.
This page documents how we use Freeseer for events and how we recommend you do too.

Equipment Needed
-------------
* A working installation of Freeseer
* VGA Capture Device

  * We recommend an `Epiphan frame grabber <http://www.epiphan.com/products/frame-grabbers/>`_
  * We use the `VGA2USB device <http://www.epiphan.com/products/frame-grabbers/vga2usb/>`_ (the red one)
    as it's the cheapest and does a decent job
* Wireless Microphones (we recommend ...)

Setup
-----

.. todo::

Preparation
-----------
* Use the Talk Editor tool to enter all the talks and their info beforehand.
* Have the speakers disable their screen saver and power saving mode.
  If the presenter's laptop goes into power saving mode,
  then the vga2usb device loses the signal and you will have to pause and restart
  the recording.

  * Linux users can use the caffeine app::

      sudo add-apt-repository ppa:caffeine-developers/ppa
      sudo apt-get update
      sudo apt-get install caffeine

Hosting the Videos
------------------
The Free and Open Source Software Learning Centre (FOSSLC) can host your videos
for free if the talks are open source related.
We promote them on `fosslc.org <http://fosslc.org>`_ and host them on YouTube.
We get quite a few hits on our website from various communities.
If you decide to use the services of FOSSLC, please email fosslc@gmail.com.

Of course, you can always use your own hosting solution.

.. todo:: when a new laptop is plugged in like when speakers are  changing between talks. The first time you press record
          sometimes vga2usb sends you a jumbled signal.
          Strangely stopping and starting the recording
          fixes it. Like the resolution is off or you don't see any useful signal just noise.
          I think restarting the recording forces it to redetect the resolution properly.

