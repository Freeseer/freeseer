Build
=====
To build the Freeseer docker image run the following command:

<pre>sudo docker build -rm -t freeseer .</pre>


Run
===
To run the Freeseer docker image run the following command:

<pre>
sudo docker run -rm -p 3000:22 -i -t -v /home/username/git/freeseer/src:/freeseer freeseer

OR

sudo docker run -rm -p 3000:22 -i -t -privileged -v /dev/video0:/dev/video0 -v /dev/bus/usb:/dev/bus/usb -v /home/zxiiro/git/freeseer/src:/freeseer freeseer
</pre>

This will port forward the SSH port to your local port 3000 allowing you to connect to the docker image.
Use <b>ssh -X root@localhost -p 3000</b> to connect.

The paramenter <b>-v source:destination</b> will mount a local directory inside the docker image. You should use this
to mount your clone of your Freeseer repo inside the image. This will allow you to use your code from inside the image.

If you need you mount a USB webcam adding the paramenters <b>-privileged -v /dev/video0:/dev/video0 -v /dev/bus/usb:/dev/bus/usb</b>
will allow you to see your USB webcam from inside the docker container.

