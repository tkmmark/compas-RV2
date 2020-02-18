================================================================================
Form Diagram
================================================================================

Create form diagram
-------------------

The form diagram defines the layout of the vertices and edges of the spatial network projected onto a horizontal plane.
RhinoVault 2 provides multiple ways to create a form diagram.
In this tutorial we create it from a skeleton. 


.. figure:: /_images/form_from_skeleton.gif
    :figclass: figure
    :class: figure-img img-fluid

* click ``form`` on the tool bar, slecet ``from_skeleton``
* Note that ``from_skeleton`` requires a skeleton to be created first. see the previous step `Skeleton <https://blockresearchgroup.github.io/compas-RV2/tutorial/skeleton/skeleton.html>`_.


Identify the supports 
---------------------

After initialising the form diagram, we identify the supports. 
For a form diagram created from skeleton, default supports have already been applied, so no operations needed here.

Update the boudary conditions
-----------------------------
Having identified the supports, we update the boundary conditions.  “feet” will be added to the support vertices.

.. figure:: /_images/update_boundaries.gif
    :figclass: figure
    :class: figure-img img-fluid

* from the drop down menu, select ``FormDiagram`` --> ``Update Boundaries`` 