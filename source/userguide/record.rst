Record
======

.. todo:: Document the Record Tool (freeseer-record)


Record Over a Network
---------------------

Via Command Line Interface (CLI)
................................

.. todo:: Document using SSH and Freeseer's CLI to record over a network.

Via Graphical User Interface (GUI)
..................................

The client tool is used for controlling Freeseer over a network.
The client connects to a running Freeseer :doc:`server`.
The server can be used to start, pause, and stop recording on multiple remote
instances of Freeseer.

To set up your client:

1. Open **freeseer-record**
2. Click **File** > **Connect to server**

.. figure:: /images/client.png
    :align: center

    *The client window*

Simply enter the host name or IP address of the server tool, enter the
passphrase, then hit `Connect`.

If you've connected to a server in the past, you can also use the `Recent
Connections` tab to select a server.

 
Report Tool
-----------

Issues can occasionally occur during a recording, such as the audio or video
not working, or perhaps the presenter does not wish to be recorded. After a
conference, it's difficult and time consuming for one person to know which
recordings have issues, especially if 100s of talks were recorded at the event.

To solve this issue, Freeseer comes with a basic reporting tool that allows the
person recording to report issues with their recordings inside the application.
This will allow whomever is uploading the recordings to quickly scan through
and find those which have issues.


Using the Report Tool
*********************

To access the report tool:

1. Open **freeseer-record**
2. Click **Help** > **Report**


.. figure:: /images/reporttool.png
    :align: center

    A basic form will open for the currently selected talk.

The form has 3 fields which need to be assessed by the reporter.

1. A textfield for a short comment describing the issue
2. A dropdown list containing options for the type of issue

   * Current options are "No Issues", "No Audio", "No Video", and
     "No Audio/Video"

3. A checkbox indicating if a Release Form was received [#release]_

After an event is complete the organizer can use the :ref:`report-editor` to
view the submitted reports.

.. rubric:: Footnotes

.. [#release] The "Release Received" checkbox was added since many events require
  presenters to sign a legal release form indicating they are giving permission
  to record their talk.
