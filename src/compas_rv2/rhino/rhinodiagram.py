from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists import MeshArtist

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector

from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier


__all__ = ["RhinoDiagram"]


class RhinoDiagram(object):

    def __init__(self, diagram):
        self.diagram = diagram
        self.artist = MeshArtist(self.diagram)

    def select_vertices(self):
        keys = VertexSelector.select_vertices(self.diagram)
        return keys

    def select_edges(self):
        keys = EdgeSelector.select_edges(self.diagram)
        return keys

    def select_faces(self):
        keys = FaceSelector.select_faces(self.diagram)
        return keys

    def update_attributes(self):
        return compas_rhino.update_settings(self.diagram.attributes)

    def update_vertices_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_vertices()
        return VertexModifier.update_vertex_attributes(self.diagram, keys, names)

    def update_edges_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_edges()
        return EdgeModifier.update_edge_attributes(self.diagram, keys, names)

    def update_faces_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_faces()
        return FaceModifier.update_face_attributes(self.diagram, keys, names)

    def draw(self, settings):
        self.artist.layer = settings.get("layers.form")
        self.artist.clear_layer()

        if settings.get("show.form.vertices", True):
            color = {}
            color.update({key: settings.get("color.form.vertices") for key in self.diagram.vertices()})
            color.update({key: settings.get("color.form.vertices:is_anchor") for key in self.diagram.vertices_where({'is_anchor': True})})
            self.artist.draw_vertices(color=color)

        if settings.get("show.form.edges", True):
            color = {}
            color.update({key: settings.get("color.form.edges") for key in self.diagram.edges()})
            self.artist.draw_edges(color=color)

        if settings.get("show.form.faces", True):
            color = {}
            color.update({key: settings.get("color.form.faces") for key in self.diagram.faces()})
            self.artist.draw_faces(color=color)

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
