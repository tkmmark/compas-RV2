================================================================================
Skeleton
================================================================================


Sketch your own form diagram
---------------------

Skeleton is a tool allowing user to quickly sketch and modify a form diagram. 


Create
======

Create a skeleton diagram from scracth. It takes Rhino lines as branch skeleton. Use mouse cursor to assgin inital width to the diagram. 

.. figure:: /_images/skeleton_create.gif
    :figclass: figure
    :class: figure-img img-fluid


* type ``RV2skeleton`` in Rhino command line / or click ``skeleton`` on the tool bar / or select from the drop down menu
* choose ``create``
* select lines in Rhino to initiate a Skeleton
* click on the leaf end, move cursor, click again to confirm the width of diagram leaf
* click on the node, move cursor, click again to confirm the width of diagram node 


Modify
======

Skeleton digarm can be modified to follow the design decision or to fit the site condition. 
Branch lines can be added to or removed from the current skeleton.


.. figure:: /_images/skeleton_modify01.gif
    :figclass: figure
    :class: figure-img img-fluid


.. figure:: /_images/skeleton_modify02.gif
    :figclass: figure
    :class: figure-img img-fluid


* type ``RV2skeleton`` in Rhino command line / or click ``skeleton`` on the tool bar / or select from the drop down menu
* choose ``modify``
* choose the operation from the options, end this round of modify with ``finish``
* Note that ``move vertex`` should always be the last step as the modification of the local details. 


To Diagram
======

After finalizing the sketch, export a form diagram from the skeleton. 
The skeleton can be edited again and be used to generate more form diagrams. 

* type ``RV2skeleton`` in Rhino command line / or click ``skeleton`` on the tool bar / or select from the drop down menu
* choose ``to_diagram``