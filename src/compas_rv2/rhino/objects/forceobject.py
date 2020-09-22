from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import i_to_rgb
import compas_rhino

from .meshobject import MeshObject


__all__ = ["ForceObject"]


class ForceObject(MeshObject):
    """Scene object for RV2 force diagrams.

    Parameters
    ----------
    diagram : :class:`compas_rv2.datastructures.ForceDiagram`
        The force diagram data structure.

    Attributes
    ----------
    artist : :class:`compas_rv2.rhino.ForceArtist`
        The specialised force diagram artist.

    Notes
    -----
    Force diagrams have two editable vertex attributes that can be modified
    by the user through the Rhino interface:

    * `x`: the X coordinate
    * `y`: the Y coordinate.

    Examples
    --------
    >>> form = ...
    >>> force = ForceDiagram.from_formdiagram(form)
    >>> scene = Scene()
    >>> scene.settings = {... this should be stuff related to the scene, not to the settings of individual nodes ...}
    >>> node = scene.add(force, name='force', settings=settings)
    >>> scene.update()
    >>> node.settings['show.vertices'] = True
    >>> node.settings['color.vertices'] = {key: (255, 0, 0) for key in node.datastructure.vertices_wehere({'is_fixed': True})}
    >>> scene.update()
    """

    SETTINGS = {
        'layer': "RV2::ForceDiagram",
        'show.vertices': True,
        'show.edges': True,
        'color.vertices': [0, 255, 255],
        'color.vertices:is_fixed': [0, 255, 255],
        'color.edges': [0, 0, 255],
    }

    def draw(self):
        layer = self.settings["layer"]
        self.artist.layer = layer
        self.artist.clear_layer()
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        # groups

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        # vertices

        vertices = list(self.mesh.vertices())
        color = {vertex: self.settings["color.vertices"] for vertex in vertices}
        guids = self.artist.draw_vertices(vertices, color)
        self.guid_vertex = zip(guids, vertices)
        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        if self.settings["show.vertices"]:
            compas_rhino.rs.ShowGroup(group_vertices)
        else:
            compas_rhino.rs.HideGroup(group_vertices)

        # edges

        edges = list(self.mesh.edges())
        color = {edge: self.settings['color.edges'] for edge in edges}

        # color analysis

        if self.scene.settings['RV2']['show.forces']:
            lengths = [self.mesh.edge_length(*edge) for edge in edges]
            lmin = min(lengths)
            lmax = max(lengths)
            for edge, length in zip(edges, lengths):
                if lmin != lmax:
                    color[edge] = i_to_rgb((length - lmin) / (lmax - lmin))

        guids = self.artist.draw_edges(edges, color)
        self.guid_edge = zip(guids, edges)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings["show.edges"]:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        # angles

        if self.scene.settings['RV2']['show.angles']:
            tol = self.scene.settings['RV2']['tol.angles']
            edges = list(self.mesh.edges())
            angles = self.mesh.edges_attribute('_a', keys=edges)
            amin = min(angles)
            amax = max(angles)
            if (amax - amin)**2 > 0.001**2:
                text = {}
                color = {}
                for edge, angle in zip(edges, angles):
                    if angle > tol:
                        text[edge] = "{:.0f}".format(angle)
                        color[edge] = i_to_rgb((angle - amin) / (amax - amin))
                guids = self.artist.draw_edgelabels(text, color)
                self.guid_edgelabel = zip(guids, edges)

        self.redraw()
