from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .meshartist import MeshArtist


__all__ = ['ForceArtist']


class ForceArtist(MeshArtist):
    """Artist for visualizing force diagrams in the Rhino model space."""

    @property
    def vertex_xyz(self):
        """dict:
        The view coordinates of the mesh vertices.
        The view coordinates default to the actual mesh coordinates.
        """
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.mesh.vertex_attributes(vertex, 'xy') + [0.0] for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    # def draw_edgelabels(self, text, color):
    #     labels = []
    #     for key in text:
    #         u, v = key
    #         a = self.mesh.vertex_attributes(u, 'xy') + [0]
    #         b = self.mesh.vertex_attributes(v, 'xy') + [0]
    #         pos = [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.0]
    #         labels.append({'pos': pos, 'text': text[key], 'name': "ForceDiagram.edgelabel", 'color': color[key]})
    #     return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
