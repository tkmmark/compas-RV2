================================================================================
Form Diagram: Part 2
================================================================================


.. figure:: /_images/flowchart.png
    :figclass: figure
    :class: figure-img img-fluid

Identify the supports and boundaries 
------------------------------------
The second part is to identify the supports of a form diagram and update the boundary conditions.


Identify the supports 
=====================

After initialising the form diagram, we identify the supports. 

* select ``Modify form diagram`` --> ``Update vertices`` from the drop down menu
* select support vertices, set ``is_fixed`` and ``is_anchor`` attribute to ``True``

For a form diagram created from skeleton, default supports have already been applied, so no operation is needed here.


Update the boudary conditions
=============================

.. figure:: /_images/update_boundaries.gif
    :figclass: figure
    :class: figure-img img-fluid

Having identified the supports, we update the boundary conditions.  “feet” will be added to the support vertices.

* from the drop down menu, select ``FormDiagram`` --> ``Update Boundaries`` 

.. literalinclude:: /_download/freeform_vault.py
    :language: python
    :lines: 99-103