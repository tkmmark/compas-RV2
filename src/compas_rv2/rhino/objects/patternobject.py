from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rhino.artists import MeshArtist


__all__ = ["PatternObject"]


class PatternObject(MeshObject):
    """Scene object for mesh-based data structures in RV2.

    Parameters
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
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

    __module__ = 'compas_rv2.rhino'

    def __init__(self, scene, pattern, **kwargs):
        super(PatternObject, self).__init__(scene, pattern, **kwargs)
        self.artist = MeshArtist(self.datastructure)

    def draw(self):
        """Draw the pattern in the Rhino scene using the current settings."""
        layer = self.settings['pattern.layer']
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings['pattern.show.vertices']:
            keys = list(self.datastructure.vertices())
            color = {key: self.settings['pattern.color.vertices'] for key in keys}
            color.update({key: self.settings['pattern.color.vertices:is_fixed'] for key in self.datastructure.vertices_where({'is_fixed': True}) if key in keys})
            color.update({key: self.settings['pattern.color.vertices:is_anchor'] for key in self.datastructure.vertices_where({'is_anchor': True}) if key in keys})
            guids = self.artist.draw_vertices(keys, color)
            self.guid_vertex = zip(guids, keys)
        else:
            guids_vertices = list(self.guid_vertex.keys())
            compas_rhino.delete_objects(guids_vertices, purge=True)
            self._guid_vertex = {}

        if self.settings['pattern.show.edges']:
            keys = list(self.datastructure.edges())
            color = {key: self.settings['pattern.color.edges'] for key in keys}
            guids = self.artist.draw_edges(keys, color)
            self.guid_edge = zip(guids, keys)
        else:
            guids_edges = list(self.guid_edge.keys())
            compas_rhino.delete_objects(guids_edges, purge=True)
            self._guid_edge = {}

        if self.settings['pattern.show.faces']:
            keys = list(self.datastructure.faces())
            color = {key: self.settings['pattern.color.faces'] for key in keys}
            guids = self.artist.draw_faces(keys, color)
            self.guid_face = zip(guids, keys)
        else:
            guids_faces = list(self.guid_face.keys())
            compas_rhino.delete_objects(guids_faces, purge=True)
            self._guid_face = {}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
