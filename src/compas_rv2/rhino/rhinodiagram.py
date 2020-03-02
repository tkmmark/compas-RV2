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

    name = None

    def __init__(self, diagram):
        self.diagram = diagram
        self.artist = MeshArtist(self.diagram)

        def initialise_attributes_properties(default_attributes):
            return {key: {'editable': False, 'type': type(default_attributes[key])} for key in default_attributes}

        self.vertex_attributes_properties = initialise_attributes_properties(self.diagram.default_vertex_attributes)
        self.edge_attributes_properties = initialise_attributes_properties(self.diagram.default_edge_attributes)
        self.face_attributes_properties = initialise_attributes_properties(self.diagram.default_face_attributes)

    def vertex_attribute_editable(self, attribute, editable=None):
        if editable is None:
            return self.vertex_attributes_properties[attribute]['editable']
        elif type(editable) == bool:
            self.vertex_attributes_properties[attribute]['editable'] = editable

    def edge_attribute_editable(self, attribute, editable=None):
        if editable is None:
            return self.edge_attributes_properties[attribute]['editable']
        elif type(editable) == bool:
            self.edge_attributes_properties[attribute]['editable'] = editable

    def face_attribute_editable(self, attribute, editable=None):
        if editable is None:
            return self.face_attributes_properties[attribute]['editable']
        elif type(editable) == bool:
            self.face_attributes_properties[attribute]['editable'] = editable

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
