from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import RhinoDiagram


__all__ = ["RhinoThrustDiagram"]


class RhinoThrustDiagram(RhinoDiagram):

    def draw(self, settings):
        self.artist.layer = settings.get("layers.thrust")
        self.artist.clear_layer()

        if settings.get("show.thrust.vertices", True):
            keys = list(self.diagram.vertices_where({'is_external': False}))
            color = {}
            color.update({key: settings.get("color.thrust.vertices") for key in self.diagram.vertices()})
            color.update({key: settings.get("color.thrust.vertices:is_fixed") for key in self.diagram.vertices_where({'is_fixed': True})})
            color.update({key: settings.get("color.thrust.vertices:is_anchor") for key in self.diagram.vertices_where({'is_anchor': True})})
            self.artist.draw_vertices(color=color)

        if settings.get("show.thrust.edges", True):
            keys = list(self.diagram.edges_where({'is_edge': True, 'is_external': False}))
            color = {}
            color.update({key: settings.get("color.thrust.edges") for key in keys})
            self.artist.draw_edges(keys=keys, color=color)

        if settings.get("show.thrust.faces", True):
            keys = list(self.diagram.faces_where({'is_loaded': True}))
            color = {}
            color.update({key: settings.get("color.thrust.faces") for key in keys})
            self.artist.draw_faces(keys=keys, color=color)

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
