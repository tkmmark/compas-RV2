================================================================================
Form Diagram: Part 1
================================================================================


.. figure:: /_images/flowchart.png
    :figclass: figure
    :class: figure-img img-fluid

Create a force pattern
----------------------

The form diagram defines the layout of the vertices and edges of the spatial network projected onto a horizontal plane.

The first part is to create a 2D force pattern. RhinoVault 2 provides several ways to create a pattern: 
`from lines`, `from mesh`, `from surface`, `from skeleton` etc. 
In this tutorial we introduce how to create a pattern from a skeleton. 


Create Skeleton
===============

.. figure:: /_images/skeleton_create.gif
    :figclass: figure
    :class: figure-img img-fluid

Skeleton is a tool allowing user to quickly sketch and modify a form diagram. 
It takes a group of single lines as input. Drag the mouse cursor to assign inital width to the diagram. 

* select ``Make form diagram`` --> ``Skeleton`` --> ``From lines`` from the drop down menu
* select all the lines
* click on the leaf end, move the cursor to get an ideal leaf width, click again to confirm
* click on the node, repeat last step to get the node width

.. literalinclude:: /_download/freeform_vault.py
    :language: python
    :lines: 55-63


Modify
======

.. figure:: /_images/skeleton_modify.gif
    :figclass: figure
    :class: figure-img img-fluid

Skeleton digarm can be modified to follow the design decision or to fit the site condition. 

* select ``Skeleton`` --> ``Modify`` from the drop down menu
* choose ``move_skeleton``, select a skeleton vertex, move it to the new locaiton
* choose ``move_vertex``, select any vertex, move it to the new locaiton. notice the difference between ``move_skeleton`` and ``move_vertex``
* choose ``subidivide``, the diagram will be subdivided and smoothed
* repeat modifications until you get the ideal form, end it by clicking on ``finish``
* Note that ``move_vertex`` should always be the last step as the modification to local details

.. literalinclude:: /_download/freeform_vault.py
    :language: python
    :lines: 69-76


Export
======

.. figure:: /_images/form_from_skeleton.gif
    :figclass: figure
    :class: figure-img img-fluid

After finishing the skeleton, we can export it to a form diagram.

* click ``form`` on the tool bar, slecet ``from_skeleton``
* Note that ``from_skeleton`` requires a skeleton to be created first.

.. literalinclude:: /_download/freeform_vault.py
    :language: python
    :lines: 98