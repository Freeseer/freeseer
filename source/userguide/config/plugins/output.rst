Output
======

WebM Output
-----------
.. todo::


Video Preview
-------------
.. todo::


Audio Feedback
--------------
.. todo::


RTMP streaming
--------------

The `Real Time Messaging Protocol (RTMP) <http://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol>`_
is a popular format for video/audio streaming. You can stream from Freeseer
to an arbitrary server using the RTMP plugin.

To enable streaming

1. Open :ref:`Freeseer's configuration <config>` and go to the "Recording" tab
2. Check the "Record to Stream" box
3. Set the stream format to "RTMP Streaming"
4. Click the "Setup" button to access more options
5. Specify the "Stream URL" (the location you'll be streaming to)

.. note:: All outputs must be set to "leaky mode".
          Go to "Plugins" > "Output" > "Video Preview" > "Leaky Queue".

Justin.tv
*********

There is built-in support for streaming to `Justin.tv <http://www.justin.tv/>`_.
To enable it, repeat the above steps 1-4, then change the
"Streaming Destination" from "custom" to "justin.tv".

You also have to input your "Streaming Key".
To get one, `log in to your Justin.tv account <http://www.justin.tv/user/login>`_
and go to http://www.justin.tv/broadcast/adv_other.

You also have the option to set your Justin.tv channel properties (stream title
and description). Check the "Set Justin.tv channel properties" box and enter
your "Consumer Key" and "Consumer Secret".

.. tip::
  To obtain a Consumer Key and Consumer Secret from Justin.tv,
  got to http://www.twitch.tv/developer/activate.

  You will need to provide login credentials for Justin.tv.
  This will make your account a developer account (as of this moment,
  this does not have any adverse effects).
  
  In order to obtain the Consumer Key and Consumer Secret,
  you will have to create an application in Justin.tv.
  To do this, go to http://www.twitch.tv/oauth_clients/create.

  On this page you will be asked to provide a name for the application and
  a set of URLs - these can be chosen arbitrarily, they serve no purpose for
  RTMP streaming. After you press "Save", you will be taken to a page where the
  Consumer Key and Consumer Secret will be shown - you can now provide
  these to Freeseer!

When you're done setting up your Justin.tv preferences in Freeseer, click the
"Apply - stream to Justin.tv" button on the bottom of the settings tab. Enjoy!


Ogg Icecast
-----------
.. todo::


Ogg Output
----------
.. todo::
