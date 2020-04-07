================================================================================
Tutorial
================================================================================

.. figure:: _images/tutorial_0.jpg
    :figclass: figure
    :class: figure-img img-fluid

This section provides a step-by-step tutorial of a simple example, highlighting and describing the main features of RV2.

|

----

0. Initializing
===============

Initiates the RV2 engine, imports all the relevant packages and activates compas_cloud server. The startup window also provides various useful links to useful information, such as the online documentation, tutorials, examples and terms of use. Don't forget to read the Terms and Conditions, and the Data Donation Agreement.

.. figure:: _images/tutorial_1.jpg
    :figclass: figure
    :class: figure-img img-fluid

----

1. Pattern
==========

1.  **Make pattern**

    A pattern is a collection of lines that define the topology of the form diagram. In this step, the user can create a pattern from: a Rhino NURBS surface object; a Rhino mesh object; from lines; from a set of boundary features (with Delaunay triangulation or compas_pattern); or skeleton.

    In this example, we will use a simple orthogonal surface, which can be created through the Rhino command, "Rectanguarl plane: corner to corner."

    .. figure:: _images/tutorial_2.jpg
        :figclass: figure
        :class: figure-img img-fluid

    In the RhinoVAULT 2 drop down menu, select "Create pattern", then "From Surface."

    .. figure:: _images/tutorial_3.jpg
        :figclass: figure
        :class: figure-img img-fluid

    This command will generate a pattern from the input surface, using the UV mapping of the surface. The user has the option to enter values for "U" and "V."

    .. figure:: _images/tutorial_4.jpg
        :figclass: figure
        :class: figure-img img-fluid

2.  **Modify pattern**

    After a pattern has been created, it can be modified for further refinement through procedures such as subdivide, relax, etc. These features will not be presented in this example.

----

2. Form and force diagrams
==========================

1.  **Define boundary conditions**

    Once a Pattern object has been generated, the boundary conditions will need to be defined. In RV2, the boundary conditions include: 1) defining the supports (vertices of the structure where reactions are allowed); and 2) loading parameters and conditions.

    In the RhinoVAULT 2 drop down menu, select "Define Boundary Conditions", then "Identify Supports."

    .. figure:: _images/tutorial_5.jpg
        :figclass: figure
        :class: figure-img img-fluid

    The command will provide two options, to select or unselect vertices to define them as supports or not. The vertex selection options are: all boundary vertices; all vertices on the selected boundary edge; and manual. Here, we use the "AllBoundaryVertices" option to turn all of the vertices on the boundary of the pattern to supports. Once the vertex has been defined as a support, it will be displayed in red.

    .. figure:: _images/tutorial_6.jpg
        :figclass: figure
        :class: figure-img img-fluid

2.  **Create form diagram**

    Once the boundary conditions have been defined, the Pattern can now be converted into a FormDiagram.

    In the RhinoVAULT 2 drop down menu, select "Create FormDiagram."

    .. figure:: _images/tutorial_7.jpg
        :figclass: figure
        :class: figure-img img-fluid

    This command will add "feet" to the support vertices, representing the horizontal components of the reactions at the supports, and generate the initial ThrustDiagram (displayed in magenta), the geometry of which is equivalent to the FormDiagram at this initial, un-equilibrated state. Notice the additionof the blue edges at the support vertices, representing the horizontal reaction components at those vertices.

    .. figure:: _images/tutorial_8.jpg
        :figclass: figure
        :class: figure-img img-fluid

3.  **Create force diagram**

    Once the FormDiagram has been created, the ForceDiagram can now be created.

    In the RhinoVAULT 2 drop down menu, select "Create ForceDiagram."

    .. figure:: _images/tutorial_9.jpg
        :figclass: figure
        :class: figure-img img-fluid

    The ForceDiagram will be automatically drawn to the right (+x) of the FormDiagram. The initial ForceDiagram is the topological dual of the FormDiagram. The two diagrams are not yet reciprocal, meaning that the corresponding edges in the diagrams are not perpendicular to the other. When the diagrams are not yet reciprocal (in another words, perpendicular-ised or "equilibrated"), the edges with angle deviations above the defined angle tolerance will be displayed (in this example, the red dots near the corners).

    .. figure:: _images/tutorial_10.jpg
        :figclass: figure
        :class: figure-img img-fluid

----

3. Equilibrium
==============

1.  **Horizontal equilibrium**

    Once the FormDiagram and ForceDiagram have been created, the horizontal equilibrium algorithm perpendicular-ises either or both diagrams, which converts them from dual to reciprocal diagrams.

    In the RhinoVAULT 2 drop down menu, select "Horizontal Equilibrium."

    .. figure:: _images/tutorial_11.jpg
        :figclass: figure
        :class: figure-img img-fluid

    Under "alpha" option, the user will be able to select a value that determine which of the two diagrams will have more weight during the perpendicular-isation process. Default is "form100," which only allows the ForceDiagram to update in its geometry. "kmax" is the number of iterations for the algorithm. Default number of iterations is 100.

    If horizontal equilibrium has been found, meaning that all the corresponding edges now have angle deviations that are below the defined angle tolerance, the two diagrams should no longer have any dots displaying the angle values, as shown below. Notice that the blue edges in the corners of the ForceDiagram on the right, is now perpendicular to the corresponding edges of the "feet" in the FormDiagram to the left.

    .. figure:: _images/tutorial_12.jpg
        :figclass: figure
        :class: figure-img img-fluid

2.  **Vertical equilibrium**

    With the FormDiagram and ForceDiagram now reciprocal, the coordinates of the ThrustDiagram can be iteratively computed based on a desired z-max (target height) value.

    In the RhinoVAULT 2 drop down menu, select "Vertical Equilibrium."

    .. figure:: _images/tutorial_13.jpg
        :figclass: figure
        :class: figure-img img-fluid

    The user can manually enter a desired value for "zmax," the desired target height of the vault. "kamx" is the number of iterations for the algorithm. Default number of iterations is 100.

    If the vertical equilibrium is successfully computed and found, the new ThrustDiagram will be displayed, now with updated z coordinates.

    .. figure:: _images/tutorial_14.jpg
        :figclass: figure
        :class: figure-img img-fluid

----

4. Interaction
==============

RV2 provides various post-form-finding functionalities to interact with the three diagrams (FormDiagram, ForceDiagram or the ThrustDiagram) to explore various design options and parameters. In this example, the geometry of the ForceDiagram will be modified to control the geometry of the FormDiagram.

1.  **Modify form diagram**

    The vertices of the form diagram can be fixed, and edges can be constrained to remain fixed in its length. The faces of the form diagram can also be used to toggle openings.

    These features will not be presented in this example.

2.  **Modify force diagram**

    One of the most powerful features of TNA is the user's ability to control the form by constraining and interacting with the force diagram. The user can fix vertices, constrain edge lengths (which sets bounds on the minimum and maximum horizontal forces in the corresponding memebers), and move vertices to manually manipulate the force distribution in the thrust diagram.

    In the RhinoVAULT 2 drop down menu, select "Modify ForceDiagram" then "Move vertices."

    .. figure:: _images/tutorial_15.jpg
        :figclass: figure
        :class: figure-img img-fluid

    The vertices can be selected by edges and its chain of continuous edges, or manually. Select manual. Select a group of vertices in the top part of the ForceDiagram, and move it up in +y direction.

    .. figure:: _images/tutorial_16.jpg
        :figclass: figure
        :class: figure-img img-fluid

    The geometry of the ForceDiagram have been updated, but the FormDiagram and ForceDiagram are no longer in horizontal equilibrium. Run "Horizontal Equilibrium" again, to perpendicular-ise the two diagrams again.

    .. figure:: _images/tutorial_17.jpg
        :figclass: figure
        :class: figure-img img-fluid

    With the FormDiagram and ForceDiagram in horizontal equilibrium, run "Vertical equilibrium" to compute the new geomerty of the ThrustDiagram. Notice now, the crease in the FormDiagram, which corresponds to the longer edges in the ForceDiagram, where the internal member forces are greater.

    .. figure:: _images/tutorial_18.jpg
        :figclass: figure
        :class: figure-img img-fluid

    This modificatoin funcationality can be applied repeatedly to continue force-driven form finding.

    .. figure:: _images/tutorial_19.jpg
        :figclass: figure
        :class: figure-img img-fluid

    Under "Settings," then "Object settings," various global parameters and visualisations options can be moidified.

    .. figure:: _images/tutorial_20.jpg
        :figclass: figure
        :class: figure-img img-fluid

    By checking on "Pipes," the edges of the ThrustDiagram can be visualised with pipes, the radii of which are proportional to the internal forces.

    .. figure:: _images/tutorial_21.jpg
        :figclass: figure
        :class: figure-img img-fluid

3.  **Modify thrust diagram**

    The user can also interact directly with the thrust diagram, to change the vertical location of the vertices, changing the fixities of vertices, and toggling openings.

    These features will not be presented in this example.

----

5. Extensions
=============

RV2, which is based on the COMPAS framework, offers a flexible and robust platform to integreate other computational methods into the form finding workflow, such as best-fit TNA analysis, laod-path optimisation and various other fabrication-related applications.

Currently under construction.