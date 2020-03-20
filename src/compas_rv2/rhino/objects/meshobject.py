from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier


__all__ = ['MeshObject']


def initialise_attributes_properties(default_attributes):
    return {key: {'editable': False, 'type': type(default_attributes[key])} for key in default_attributes}


class MeshObject(object):

    def __init__(self, scene, datastructure, name=None, visible=True, **kwargs):
        self.scene = scene
        self.datastructure = datastructure
        self.artist = None
        self.name = name
        self.visible = visible
        self.vertex_attributes_properties = initialise_attributes_properties(self.datastructure.default_vertex_attributes)
        self.edge_attributes_properties = initialise_attributes_properties(self.datastructure.default_edge_attributes)
        self.face_attributes_properties = initialise_attributes_properties(self.datastructure.default_face_attributes)

    @property
    def settings(self):
        return self.scene.settings

    def draw(self):
        raise NotImplementedError

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
        """Manually select vertices in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected vertices.

        Examples
        --------
        >>>
        """
        keys = VertexSelector.select_vertices(self.datastructure)
        return keys

    def select_edges(self):
        """Manually select edges in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected edges.

        Examples
        --------
        >>>
        """
        keys = EdgeSelector.select_edges(self.datastructure)
        return keys

    def select_faces(self):
        """Manually select faces in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected faces.

        Examples
        --------
        >>>
        """
        keys = FaceSelector.select_faces(self.datastructure)
        return keys

    def update_attributes(self):
        return compas_rhino.update_settings(self.datastructure.attributes)

    def update_vertices_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_vertices()
        return VertexModifier.update_vertex_attributes(self.datastructure, keys, names)

    def update_edges_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_edges()
        return EdgeModifier.update_edge_attributes(self.datastructure, keys, names)

    def update_faces_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_faces()
        return FaceModifier.update_face_attributes(self.datastructure, keys, names)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
