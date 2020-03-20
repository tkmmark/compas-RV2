from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rhino.artists import MeshArtist


__all__ = ["PatternObject"]


class PatternObject(MeshObject):

    def __init__(self, scene, pattern, **kwargs):
        super(PatternObject, self).__init__(scene, pattern, **kwargs)
        self.artist = MeshArtist(self.datastructure)

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
