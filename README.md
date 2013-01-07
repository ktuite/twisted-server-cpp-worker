twisted-server-cpp-worker
=========================

Some sample code of a webserver (written in python using Twisted) that does computation via an external c++ worker client. 

Files:

    mainServer.py
This is a short example webserver with one root resource at "http://localhost:8080/random"

    workerManager.py
Another python class that handles communication with the remote worker

    workerClient.cpp
C++ example client that starts up and connects to the mainServer/workerManager, which is listening on a particular port.

    workerClient.py
The same sort of example worker client but written in python instead of C++.
