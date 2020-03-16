from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas_rhino.artists import MeshArtist
from compas_rv2.rhino import RhinoDiagram


__all__ = ["RhinoThrustDiagram"]


class ThrustArtist(MeshArtist):

    def draw_external(self, scale=1.0):
        lines = []
        for key in self.mesh.vertices_where({'is_anchor': True}):
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector([0, 0, r[2]], scale))
            lines.append({
                "start": a,
                "end": b,
                "color": (0, 255, 255),
                "arrow": "start"
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # def draw_pipes(self, scale=1.0):
    #     pipes = []
    #     for u, v in self.mesh.edges_where({'is_edge': True}):
    #         pipes.append({
    #             'start':
    #         })

    def draw_residual(self, scale=1.0):
        lines = []
        for key in self.mesh.vertices_where({'is_anchor': False, 'is_external': False}):
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector([0, 0, r[2]], scale))
            lines.append({
                "start": a,
                "end": b,
                "color": (0, 255, 255),
                "arrow": "start"
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)


class RhinoThrustDiagram(RhinoDiagram):

    def __init__(self, diagram):
        super(RhinoThrustDiagram, self).__init__(diagram)
        self.artist = ThrustArtist(self.diagram)

    def draw(self, settings):
        self.artist.layer = settings.get("layers.thrust")
        self.artist.clear_layer()

        print(settings)
        print(self.artist.layer)

        if settings.get("show.thrust.vertices", True):
            keys = list(self.diagram.vertices_where({'is_external': False}))
            color = {}
            color.update({key: settings.get("color.thrust.vertices") for key in self.diagram.vertices()})
            color.update({key: settings.get("color.thrust.vertices:is_fixed") for key in self.diagram.vertices_where({'is_fixed': True})})
            color.update({key: settings.get("color.thrust.vertices:is_anchor") for key in self.diagram.vertices_where({'is_anchor': True})})
            self.guid_vertices = self.artist.draw_vertices(color=color, keys=keys)

        if settings.get("show.thrust.edges", True):
            keys = list(self.diagram.edges_where({'is_edge': True, 'is_external': False}))
            color = {}
            color.update({key: settings.get("color.thrust.edges") for key in keys})
            self.guid_edges = self.artist.draw_edges(keys=keys, color=color)

        if settings.get("show.thrust.faces", True):
            keys = list(self.diagram.faces_where({'is_loaded': True}))
            color = {}
            color.update({key: settings.get("color.thrust.faces") for key in keys})
            self.guid_faces = self.artist.draw_faces(keys=keys, color=color)

        if settings.get("show.thrust.external", True):
            self.artist.draw_external(scale=settings.get("scale.thrust.external", 1.0))

        # if settings.get("show.thrust.residual", True):
        #     self.artist.draw_residual(scale=settings.get("scale.thrust.residual", 1.0))

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
