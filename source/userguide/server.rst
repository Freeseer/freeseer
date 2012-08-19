Server
======


Introduction
............

This tool is used for controlling Freeseer Record over network. 
The server can start recording, pause recording and stop recording.
If you want the instance of your freeseer recorder to be controlled you can follow these steps:

How to remote control:
.......

1. Open **freeseer-server**

.. figure:: /images/server_s1.png
    :align: center

    You will be faced with this interface
Before clicking "Start Server" button, you can choose the IP you would like to use from the combobox next to the "IP:" label
After you choose the ip or leaving the default you will have to click "Start Server". This will initialize and start our server.

.. figure:: /images/server_s2.png
    :align: center

    This is how the server looks when it is running.

.. figure:: /images/server_s3.png
    :align: center

    A client is connected.
From here we can tell the client to start recording, pause recording or stop recording. Client's status is shown next to the IP address of the client.
Right now client is idle so we can start recording. 
When "Start Recording" button is pressed, client's status will change. Acording to the client's status, the buttons will updated with the appropriate labels.
Client can also be disconnected if "Disconnect" button is triggered. Client can also be disconnect from the server from client side.

.. figure:: /images/server_s4.png
    :align: center

    Here client is in recording state.
When client is recording we could pause or stop recording. Triggering the appropriate button will send the action to the client.


.. figure:: /images/server_s5.png
    :align: center

    When recording is paused it can be resumed or it can be stopped.

