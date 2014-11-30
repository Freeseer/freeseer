Notes on the Freeseer Server/Client
===================================

Freeseer will eventually be headlessly configurable and controllable via its REST API. We use Zeroconf protocol to alert Clients of any running Freeseer hosts, as well as their IP and Port. This article denotes the environment requirements, and instructions for running Freeseer as a headless server. Furthermore, I will explain how the Freeseer browser mechanism works, on how Freeseer is seen by Zeroconf/Bonjour more generally.

Running the Freeseer Server
---------------------------

**OS Requirements**

The Freeseer server can only be run on Linux boxes because of a dependency on Avahi. 

**Dependencies**

The Freeseer server requires the following packages to be installed::

 avahi-daemon
 python-avahi

**Instructions**

Ensure ``avahi-daemon`` is running.
The Freeseer server is run in the command line with:: 

 freeseer server

Your box should now have an http server that accepts API requests and is broadcast over Zeroconf protocol.

On the servers box, the http server can be accessed at http://0.0.0.0:7079
On any client's box, the http server can be accessed at http://<hosts_ip>:7079

Finding Freeseer hosts on Your Network
--------------------------------------

We have yet to develop a client that can control our server headlessly, however there is a function in Freeseer that lets us browse any Freeseer hosts broadcasting on our network. This browse function makes use of the python library ``zeroconf``, and should be modified to be used with the client we eventually develop. 

**Dependencies**

The key dependency for server browsing is the python library ``zeroconf``.
Dependencies are automatically installed by running::

 pip install -Ur dev_requirements.txt 

in the folder where ``dev_requirements.txt`` is found.

**Running Host Browser**

To list any running Freeseer servers on your network::

  freeseer browse

**Notes on Advertising/Browsing**

During browsing, the ``zeroconf`` library searches for any services running with the service type ``_freeseer._tcp``. If there are any on the network, it will be found and printed to the user. If you run into any issues with clients browsing Freeseer Hosts, it is a good idea to check if your client's computer also sees the Freeseer host running. On linux, we can do this with the following command::

 avahi-browse -t _freeseer._tcp

