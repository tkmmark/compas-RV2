================================================================================
Workflow
================================================================================

.. figure:: /_images/rv2_workflow.jpg
    :figclass: figure
    :class: figure-img img-fluid


The RV2 workflow can be broken down into five main steps.

|


----


0. Initializing
===============

**Initialising RV2**
    Initiates the RV2 engine, imports all the relevant packages and activates compas_cloud server. The startup window also provides various useful links to useful information, such as the online documentation, tutorials, examples and terms of use.

**Global settings**


**Visualisation settings**


**compas_cloud**


|


----


1. Pattern
==========

**Make pattern**
    A pattern is a collection of lines that define the topology of the form diagram. In this step, the user can create a pattern from: a Rhino NURBS surface object; a Rhino mesh object; from lines; from a set of boundary features (with Delaunay triangulation or compas_pattern); or skeleton.

**Modify pattern**
    After a pattern has been created, it can be modified for further refinement through procedures such as subdivide, relax, etc.

|


----


2. Form and force diagrams
==========================

**Define boundary conditions**
    In this step, the user defines the support vertices, open edges and loading conditions.

**Create form diagram**
    Once the boundary conditions have been defined, the pattern now becomes a form diagram object.

**Create force diagram**
    Using the form diagrm, the force diagram can be created, which is the topological dual of the form diagram.

|

----


3. Equilibrium
==============

**Horizontal equilibrium**
    Once the form and force diagram have been created, the horizontal equilibrium parallel-izes either or both diagrams.

**Vertical equilibrium**
    With the parallel-ized form and force diagrams, the coordinates of the thrust diagram can be iteratively computed based on a desired z-max value.

|


----


4. Interaction
==============

**Modify form diagram**
    The vertices of the form diagram can be fixed, and edges can be constrained to remain fixed in its length. The faces of the form diagram can also be used to toggle openings.


**Modify force diagram**
    One of the most powerful features of TNA is the user's ability to control the form by constraining and interacting with the force diagram. The user can fix vertices, constrain edge lengths (which sets bounds on the minimum and maximum horizontal forces in the corresponding memebers), and move vertices to manually manipulate the force distribution in the thrust diagram.


**Modify thrust diagram**
    The user can also interact directly with the thrust diagram, to change the vertical location of the vertices, changing the fixities of vertices, and toggling openings.

|


----


5. Extensions
=============

RV2, which is based on the COMPAS framework, offers a flexible and robust platform to integreate other computational methods into the form finding workflow, such as best-fit TNA analysis, laod-path optimisation and various other fabrication-related applications. Currently under construction.





