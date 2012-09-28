Server
======

The *Freeseer Server* tool communicates with the :doc:`Freeseer Record </userguide/record>` tool over a network.
The server can be used to **start**, **stop**, **pause**, and **resume recording**.

Dependencies
------------

The PassLib library is required to run the server.

To install it using pip::

    sudo pip install passlib

To install it using easy_install::

    sudo easy_install passlib

.. todo:: Add MS instructions

Usage
-----

1. Open **freeseer-server**

.. figure:: /images/server_s1.png
    :align: center

    The server interface will appear.

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

