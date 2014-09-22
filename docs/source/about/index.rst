About Freeseer
==============

.. sidebar:: Software with a Purpose.

    Development of Freeseer is led by the `Free and Open Source Software Learning Centre (FOSSLC) <http://fosslc.org>`_,
    a non-profit whose vision is to improve lives with open source.
    FOSSLC also specializes in technology and know-how to record conferences with excellent quality.

    From large conferences with hundreds of talks to presentations in classrooms,
    anyone can use Freeseer to capture talks.

`Freeseer <http://freeseer.readthedocs.org>`_ (pronounced *free-see-ar*) is a free, open source, cross-platform application that
captures or streams your desktop. It's designed for capturing presentations, and has been succesfully used at many
open source conferences to record hundreds of talks (which can be seen at `fosslc.org <http://fosslc.org>`_).
Though designed for capturing presentations, it can also be used to capture demos, training materials, lectures, and other videos.

Freeseer is written in Python, uses Qt4 for its GUI, and Gstreamer for video/audio processing.
Freeseer is based on open standards and supports royalty free audio and video codecs.

Freeseer's source code is licensed under the `GNU General Public License <http://www.gnu.org/licenses/gpl.html>`_ and
is available on `GitHub <http://github.com/Freeseer/freeseer>`_.


Who We Are
----------

We're an open source community of developers, writers, designers, bloggers, students, and open source enthusiasts
whose goal is to make meaningful software with world-class documentation (inspired by ThinkUp and GitHub).

You're reading the very beginning of that effort. This documentation is an incomplete, work-in-progress. Please
join us and help :doc:`fill in the gaps </contribute/index>`.


Why We Exist
------------

FOSSLC has been recording conferences since 2008, but they weren't quite happy with their recording solutions.
There were issues such as costs, ownership, portability, and simplicity. There had to be a better way.

Freeseer began in 2009 as an in-house solution for FOSSLC to record conference talks.
Many people have contributed since then and development is still on-going.

.. seealso::
   `Freeseer's history <http://fosslc.org/drupal/node/596>`_


Expectations Around Sharing Freeseer
------------------------------------

The Freeseer project includes code, documentation, and more, written by many different people.
All Freeseer contributors retain copyright on their contributions, but agree to release it under the same license as Freeseer.
If you are unable or unwilling to contribute a patch under the GPL version 3 or later, do not submit a patch.

Freeseer is copyrighted by `FOSSLC <http://fosslc.org>`_ and various contributors (listed above).

Freeseer is licensed under the GNU General Public License, version 3 (GPLv3); you may not use this work except in compliance with the GPLv3.

You may obtain a copy of the GPLv3  at:

http://www.fsf.org/licensing/licenses/gpl.html


Who Freeseer Is For
-------------------

Freeseer can be used by everyone but is aimed at organizations and personalities who are actively involved in
conferences or events and have to record many presentations and talks in a short period of time.

Freeseer will be most useful for:

**Presenters** who want to record their own talks using a simple application that has virtually no learning curve,
and covers all their basic needs.

**Conference Staff** who want easier ways to manage the recording of talks, and record talks with top audio and video quality.

**Instructors** like professors, bloggers, or consultants who want an easy way to record their lectures, tutorials, or training material
to later share with others.


What Freeseer Can Do
--------------------

.. topic:: Introduction to Freeseer v2.5 (outdated video, but still demonstrates the essence of Freeseer)

   .. raw:: html

      <iframe type="text/html" width="100%" height="500"
       src="http://www.youtube-nocookie.com/embed/wOr1ZeQG__k?rel=0&autohide=1&showinfo=0&theme=light"
       frameborder="0"></iframe>

At its heart, Freeseer is a screencasting tool. Freeseer helps you record your desktop and audio,
whether you're recording hundreds of talks at a conference or making a how-to video at home.

Using Freeseer, you can:

**Record Talks:** The recording interface is designed to be simple so you can focus on recording. You can also pause and resume
recordings. Did we mention that the audio and video quality are great?

**Manage Talks:** Freeseer allows you to add a list of talks before you record them. Then when you're ready to record,
you simply select the talk from the list and start recording. This allows all talks to be added from beforehand, so when
it's time to present you can focus on recording and not worry about distractions (such as filling in the talk info).
You can see why Freeseer is great for recording many talks right after another.

The Talk Editor tool allows you to manually add talks, load them via RSS (a lot of conferences have an event schedule online),
or load them from a CSV file. You can also edit or remove talks. Talks are neatly displayed in a table and are sortable
by title, speaker, event, room, and more.

**Configure Freeseer:** Configure your audio and video input, output, save location, and more. With Freeseer's plugin system,
developers can easily write their own plugin to add a new feature. Plugins are configurable via the config tool.

Recording Events
----------------

.. toctree::
   :maxdepth: 2

   record
