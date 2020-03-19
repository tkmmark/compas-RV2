from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import RhinoDiagram


__all__ = ["RhinoForceDiagram"]


class RhinoForceDiagram(RhinoDiagram):

    def draw(self, settings):
        self.artist.layer = settings.get("force.layer")
        self.artist.clear_layer()

        if settings.get("force.show.vertices", True):
            color = {}
            color.update({key: settings.get("force.color.vertices") for key in self.diagram.vertices()})
            self.guid_vertices = self.artist.draw_vertices(color=color)

        if settings.get("force.show.edges", True):
            keys = list(self.diagram.edges())
            color = {}
            for key in keys:
                u_, v_ = self.diagram.primal.face_adjacency_halfedge(*key)
                if self.diagram.primal.vertex_attribute(u_, 'is_external') or self.diagram.primal.vertex_attribute(v_, 'is_external'):
                    color[key] = settings.get("force.color.edges:is_external")
                else:
                    color[key] = settings.get("force.color.edges")
            self.guid_edges = self.artist.draw_edges(keys=keys, color=color)

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
