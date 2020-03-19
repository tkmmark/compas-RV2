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


__all__ = ["PatternObject"]


# the object should bind all scene related functionality
class PatternObject(object):

    # why are these class attributes?
    name = None
    visible = True

    def __init__(self, pattern):
        self.mesh = pattern  # this is like "data" in Blender
        self.artist = MeshArtist(self.mesh)

        # this needs to be better documented
        # it is not very transparent currently
        def initialise_attributes_properties(default_attributes):
            return {key: {'editable': False, 'type': type(default_attributes[key])} for key in default_attributes}

        self.vertex_attributes_properties = initialise_attributes_properties(self.mesh.default_vertex_attributes)
        self.edge_attributes_properties = initialise_attributes_properties(self.mesh.default_edge_attributes)
        self.face_attributes_properties = initialise_attributes_properties(self.mesh.default_face_attributes)

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
        >>> scene = Scene()
        >>> pattern = Pattern.from_rhinomesh(guid)
        >>> scene.add(pattern, name='pattern')
        >>> scene.update()
        >>> obj = scene.get('pattern')
        >>> obj.mesh is pattern
        True
        >>> keys = obj.select_vertices()
        """
        keys = VertexSelector.select_vertices(self.mesh)
        return keys

    def select_edges(self):
        keys = EdgeSelector.select_edges(self.mesh)
        return keys

    def select_faces(self):
        keys = FaceSelector.select_faces(self.mesh)
        return keys

    def update_attributes(self):
        return compas_rhino.update_settings(self.mesh.attributes)

    def update_vertices_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_vertices()
        return VertexModifier.update_vertex_attributes(self.mesh, keys, names)

    def update_edges_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_edges()
        return EdgeModifier.update_edge_attributes(self.mesh, keys, names)

    def update_faces_attributes(self, keys=None, names=None):
        if not keys:
            keys = self.select_faces()
        return FaceModifier.update_face_attributes(self.mesh, keys, names)

    def draw(self, settings):
        layer = settings.get('pattern.layer')
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()
        if settings.get('pattern.show.vertices', True):
            self.artist.draw_vertices()
        if settings.get('pattern.show.edges', True):
            self.artist.draw_edges()
        if settings.get('pattern.show.faces', True):
            self.artist.draw_faces()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
