.. _record-tool:

Record
======

Record Interface
----------------

The Freeseer recording interface provides the main window for recording a
video. This interface is designed with features that enable you to record
talks at a conference very easily.

.. figure:: /images/record.png
  :align: center
  :alt: Freeseer's recording interface

  *Freeseer's Recording interface with a sample talk loaded*


.. figure:: /images/record-annotated.png
  :align: center
  :alt: Freeseer's recording interface with annotations

  *Freeseer's Recording interface with notes*

Select a Talk
*************

Typically the first task is to **find the talk you want to record** out of all
the possible talks that are stored in the Freeseer database.
You can **filter the list of talks** by selecting an **Event**, **Room**, and
then a **Date** from the dropdown lists.

.. note::
  When you record a talk, the output file will contain some of the associated
  talk data as metadata.

.. tip::
  You can enter new talks or modify existing talks using the :ref:`talk-editor` tool.

  Conferences typically release information about their talks prior
  to the event. It's good practice to enter such data (e.g. title, speaker,
  event, etc.) for every talk you plan to record, prior to attending the
  conference rather than last minute.

Audio Feedback
**************

At the bottom right of the interface there is a checkbox with a headphones icon.
Checking this will enable audio feedback, which will play any sounds being
recorded back to your speakers. This is useful if you need to check the audio
levels. We recommend using headphones when using this feature.

.. important::
  - You cannot enable or disable audio feedback while recording; the checkbox
    will be locked
  - Audio feedback is only audible while recording


Status Area
***********

At the bottom of the interface where it says "Idle", is the status area.
It shows information such as what state the program is in and how much free
space is remaining once you start recording.

Recording Controls
******************

Pressing "Prepare to Record" will initialize the Freeseer recording backend.
Freeseer has to be "prepared" to record because of a technical limitation.

.. figure:: /images/record-prepare.png
	:align: center

	*Freeseer is ready to record*

Once "Prepare to Record" is clicked, new buttons "Record" and "Pause" will
replace the "Prepare to Record" button.

Click "Record" to begin recording.

During a recording you can click "Pause" to pause the recording and resume it at
a later time. This is useful if presentation contains a break period.

.. figure:: /images/record-recording.png
	:align: center

	*Freeseer shows a Stop button during recording*

When a recording is in progress the "Record" button will change into a "Stop"
button. Clicking this will stop recording and Freeseer's interface will return
to its initial state.

 
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
********************************

.. todo:: Document using SSH and Freeseer's CLI to record over a network.

Via Graphical User Interface (GUI)
**********************************

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
