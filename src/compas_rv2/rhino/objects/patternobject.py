from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from .meshobject import MeshObject


__all__ = ["PatternObject"]


class PatternObject(MeshObject):
    """Scene object for mesh-based data structures in RV2.

    Parameters
    ----------
    pattern : :class:`compas_rv2.datastructures.Pattern`
        The pattern data structure.

    Attributes
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    pattern : :class:`compas_rv2.datastructures.Pattern`
        The pattern data structure.
    artist : :class:`compas_rv2.rhino.PatternArtist`
        The specialised pasttern artist.
    """

    SETTINGS = {
        'layer': "RV2::Pattern",
        'show.vertices': True,
        'show.edges': True,
        'show.faces': False,
        'color.vertices': [255, 255, 255],
        'color.vertices:is_anchor': [255, 0, 0],
        'color.vertices:is_fixed': [0, 0, 255],
        'color.vertices:is_constrained': [0, 255, 255],
        'color.edges': [0, 0, 0],
        'color.faces': [200, 200, 200],
        'from_surface.density.U': 10,
        'from_surface.density.V': 10,
    }

    def draw(self):
        layer = self.settings['layer']
        self.artist.layer = layer
        self.artist.clear_layer()
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        # groups

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)
        group_faces = "{}::faces".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if not compas_rhino.rs.IsGroup(group_faces):
            compas_rhino.rs.AddGroup(group_faces)

        # vertices

        vertices = list(self.mesh.vertices())
        color = {vertex: self.settings['color.vertices'] for vertex in vertices}
        color_fixed = self.settings['color.vertices:is_fixed']
        color_anchor = self.settings['color.vertices:is_anchor']
        color.update({vertex: color_fixed for vertex in self.mesh.vertices_where({'is_fixed': True})})
        color.update({vertex: color_anchor for vertex in self.mesh.vertices_where({'is_anchor': True})})

        guids = self.artist.draw_vertices(vertices, color)
        self.guid_vertex = zip(guids, vertices)
        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        if self.settings['show.vertices']:
            compas_rhino.rs.ShowGroup(group_vertices)
        else:
            compas_rhino.rs.HideGroup(group_vertices)

        # edges

        edges = list(self.mesh.edges())
        color = {edge: self.settings['color.edges'] for edge in edges}

        guids = self.artist.draw_edges(edges, color)
        self.guid_edge = zip(guids, edges)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings['show.edges']:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        # faces

        faces = list(self.mesh.faces())
        color = {face: self.settings['color.faces'] for face in faces}

        guids = self.artist.draw_faces(faces, color)
        self.guid_face = zip(guids, faces)
        compas_rhino.rs.AddObjectsToGroup(guids, group_faces)

        if self.settings['show.faces']:
            compas_rhino.rs.ShowGroup(group_faces)
        else:
            compas_rhino.rs.HideGroup(group_faces)

        self.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
