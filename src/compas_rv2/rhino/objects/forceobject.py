from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ForceArtist


__all__ = ["ForceObject"]


class ForceObject(MeshObject):

    def __init__(self, scene, diagram, **kwargs):
        super(ForceObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ForceArtist(self.datastructure)
        self.vertex_attribute_editable('x', True)
        self.vertex_attribute_editable('y', True)

    def draw(self):
        layer = self.settings.get("force.layer")
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings.get("force.show.vertices", True):
            color = {}
            color.update({key: self.settings.get("force.color.vertices") for key in self.diagram.vertices()})
            self.guid_vertices = self.artist.draw_vertices(color=color)

        if self.settings.get("force.show.edges", True):
            keys = list(self.diagram.edges())
            color = {}
            for key in keys:
                u_, v_ = self.diagram.primal.face_adjacency_halfedge(*key)
                if self.diagram.primal.vertex_attribute(u_, 'is_external') or self.diagram.primal.vertex_attribute(v_, 'is_external'):
                    color[key] = self.settings.get("force.color.edges:is_external")
                else:
                    color[key] = self.settings.get("force.color.edges")
            self.guid_edges = self.artist.draw_edges(keys=keys, color=color)

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
