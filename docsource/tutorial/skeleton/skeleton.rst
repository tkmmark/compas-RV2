================================================================================
Skeleton
================================================================================

Sketch a form diagram
----------------------------

Skeleton is a tool allowing user to quickly sketch and modify a form diagram. 

Create
======

Create a skeleton diagram from scracth. It takes Rhino lines as input. Drag the mouse cursor to assgin inital width to the diagram. 


.. figure:: /_images/skeleton_create.gif
    :figclass: figure
    :class: figure-img img-fluid


* select ``Skeleton`` --> ``From lines`` from the drop down menu
* select all the lines
* click on the leaf end, move the cursor to get an ideal leaf width, click again to confirm
* click on the node, repeat last step to get the node width


Modify
======

Skeleton digarm can be modified to follow the design decision or to fit the site condition. 


.. figure:: /_images/skeleton_modify.gif
    :figclass: figure
    :class: figure-img img-fluid

* select ``Skeleton`` --> ``Modify`` from the drop down menu
* choose ``move_skeleton``, select a skeleton vertex, move it to the new locaiton
* choose ``move_vertex``, select any vertex, move it to the new locaiton. notice the difference between ``move_skeleton`` and ``move_vertex``
* choose ``subidivide``, the diagram will be subdivided and smoothed
* repeat modifications until you get the ideal form, end it by clicking on ``finish``
* Note that ``move_vertex`` should always be the last step as the modification to local details
