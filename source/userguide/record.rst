.. _record-tool:

Record
======

The Freeseer recording interface provides the main window for recording a
video. This interface is designed with features that enable you to record
a conference very easily.


.. figure:: /images/record.png
	:align: center

	*Freeseer Recording Interface*

The typical workflow is to select a filter for the Event > Room > Date of
the Event you are recording. Which will filter down a list of *Talks*
available for the filter selected. This data is generally pre-inputted via
the :ref:`talk-editor`. It is good practice to pre-fill this data before
an event as this data will be used to populate metadata in the final output
of your recording file.

At the bottom right there is a checkbox with a image of headphones. Checking
this will enable audio feedback which will play the sounds being recorded back
to your speakers. This is useful if you need to check audio levels while a
recording is in progress. When using this feature it is recommended to plug in
headphones.

At the bottom of the interface where there is text "Idle" this is the status
area. Information from Freeseer will be displayed here while the recording is
in progress.

Finally pressing "Prepare to Record" will initialize the Freeseer recording
backend.

.. figure:: /images/record-prepare.png
	:align: center

	*Freeseer Prepare to Record*

Once "Prepare to Record" is clicked new buttons "Record" and "Pause" will
replace the "Prepare to Record" button.

Clicking "Record" will begin recording.

During a recording you can click "Pause" to pause the recording. This is useful
if a Talk is long and the speaker has decided to put a break in the presentation.

.. figure:: /images/record-recording.png
	:align: center

	*Freeseer Stop Button*

Once a recording is in progress the "Record" button will change into a "Stop"
button. Clicking this will stop recording and shutdown the recording backend.

You will be returned to the initial state of Freeseer Recording Interface at
this point.

 
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

    A basic form will open for the currently selected talk.

The form has 3 fields which need to be assessed by the reporter.

1. A textfield for a short comment describing the issue
2. A dropdown list containing options for the type of issue

   * Current options are "No Issues", "No Audio", "No Video", and
     "No Audio/Video"

3. A checkbox indicating if a Release Form was received [#release]_

After an event is complete the organizer can use the :ref:`report-editor` to
view the submitted reports.

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

.. rubric:: Footnotes

.. [#release] The "Release Received" checkbox was added since many events require
  presenters to sign a legal release form indicating they are giving permission
  to record their talk.
