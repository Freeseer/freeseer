Record
======

.. todo:: document freeseer-record

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
*************************

To access the report tool:

1. Open **freeseer-record**
2. Click **Help** > **Report**


.. figure:: /images/reporttool.png
    :align: center

    A basic form will open for the currently selected talk.

The form has 3 fields which need to be assessed by the reporter.

1. A textfield for a short comment describing the issue
2. A dropdown list containing options for the type of issue

   * Current options are "No Issue", "No Audio", "No Video", and
     "No Audio/Video"

3. A checkbox indicating if a Release Form was received [#release]_

After an event is complete the organizer can use the :ref:`report-editor` to
view the submitted reports.

.. rubric:: Footnotes

.. [#release] The "Release Received" checkbox was added since many events require
  presenters to sign a legal release form indicating they are giving permission
  to record their talk.
.. Typically this option is used with the "No Issue" flag unless there are issues with the recording.
.. TODO: Review the above line before adding it back, I find it confusing.

Client
......

This tool is used for controlling Freeseer over network. The client is for connecting to the running Freeseer Server. The server can start recording, pause recording and stop recording. If you want the instance of your freeseer recorder to be controlled you can follow these steps:

1. Open **freeseer-record**
2. Click **File** > **Client**

.. figure:: /images/client_s1.png
    :align: center

    When you see this window, you can start the client by clicking the Start button.

There are 3 ways to enter the details of the Server:

1. By entering the information to the IP, port and Passphrase textboxes.
2. Properties box can be used to enter the details quickly. This is a feature used with the properties from the Server properties box. You can copy and paste the properties and click the add properties button and the information will be entered in the appropriate textboxs.

.. figure:: /images/client_s2.png
    :align: center

3. If you have used this feature before and successfully connected to the Freeseer Server it will be on the recent connections box. You can choose the one that you would like to connect to from the list and the appropriate textboxs will be filled with the information.

.. figure:: /images/client_s3.png
    :align: center

