********************************************************************************
0. Initializing
********************************************************************************


----

Initializing RV2
================


.. figure:: /_images/rv2init.png
    :figclass: figure
    :class: figure-img img-fluid


Initializing RV2 command is required to run at the beginning of all RV2 sessions. It does several necessary jobs: 

* Bring up a front-page providing useful links about RV2 and require users to accept RV2's Terms and Agreements to proceed.

* Initialize data structures and user session needed for RV2 to operate in Rhino environment.

* Kick off **compas_cloud** server in background and establish connection to it from Rhino.

----

Settings
========

Settings menu provides interfaces to adjust global settings of RV2:

.. figure:: /_images/object_settings.png
    :figclass: figure
    :class: figure-img img-fluid

* Object Settings provides options to adjust visualization style of different RV2 objects such as Pattern, FormDiagram, ForceDiagram etc.

.. figure:: /_images/solver_settings.png
    :figclass: figure
    :class: figure-img img-fluid

* Solver Settings provides options to adjust RV2 Solver settings like kmax value for horizontal equilibrium in **compas_tna** solver.

----

compas_cloud
============

**compas_cloud** is an essential infrastructure component used by RV2. 
It runs a background server for executing highly efficient numerical algorithms from Cython packges such as **numpy** and **scipy** that are not compatible with IronPython that runs inside Rhino.
This allows RV2 to utilise full capacity of other compas packages such as **compas_tna** and **compas_triangle** which has Cython dependencies.
compas_cloud server communicates with Rhino through websocket protocol, and can be controlled from RV2 menu: 

.. figure:: /_images/compas_cloud.png
    :figclass: figure
    :class: figure-img img-fluid

* Cloud > Check: check if connection to compas_cloud server is healthy.

* Cloud > Restart: Restart compas_cloud server, with options of running in background or in a prompt console which is handy for debugging.

* Cloud > Shut Down: Shutdown the compas_cloud server.
