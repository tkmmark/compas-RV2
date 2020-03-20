from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import MeshObject
from compas_rv2.rhino import ThrustArtist


__all__ = ["ThrustObject"]


class ThrustObject(DiagramObject):

    def __init__(self, scene, diagram, **kwargs):
        super(ThrustObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ThrustArtist(self.datastructure)

    def draw(self):
        layer = self.settings.get('thrust.layer')
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings.get('thrust.show.vertices', True):
            keys = list(self.datastructure.vertices_where({'is_external': False}))
            color = {}
            color.update({key: self.settings.get('thrust.color.vertices') for key in self.datastructure.vertices()})
            color.update({key: self.settings.get('thrust.color.vertices:is_fixed') for key in self.datastructure.vertices_where({'is_fixed': True})})
            color.update({key: self.settings.get('thrust.color.vertices:is_anchor') for key in self.datastructure.vertices_where({'is_anchor': True})})
            self.guid_vertices = self.artist.draw_vertices(color=color, keys=keys)

        if self.settings.get('thrust.show.edges', True):
            keys = list(self.datastructure.edges_where({'is_edge': True, 'is_external': False}))
            color = {}
            color.update({key: self.settings.get('thrust.color.edges') for key in keys})
            self.guid_edges = self.artist.draw_edges(keys=keys, color=color)

        if self.settings.get('thrust.show.faces', True):
            keys = list(self.datastructure.faces_where({'is_loaded': True}))
            color = {}
            color.update({key: self.settings.get('thrust.color.faces') for key in keys})
            self.guid_faces = self.artist.draw_faces(keys=keys, color=color)

        if self.settings.get('thrust.show.external', True):
            self.artist.draw_external(scale=self.settings.get('thrust.scale.external', 1.0))

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
