from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.artists.meshartist import MeshArtist


__all__ = ['FormArtist']


class FormArtist(MeshArtist):
    """Artist for visualizing form diagrams in the Rhino model space."""

    def draw_vertices(self, keys, color):
        """Draw form diagram vertices in the Rhino model space.

        Parameters
        ----------
        keys : list
            The keys of the vertices that should be visualized.
        color : dict
        """
        points = []
        for key in keys:
            xy = self.mesh.vertex_attributes(key, 'xy')
            points.append({'pos': xy + [0], 'name': "FormDiagram.vertex", 'color': color[key]})
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, keys, color):
        lines = []
        for key in keys:
            u, v = key
            start = self.mesh.vertex_attributes(u, 'xy') + [0]
            end = self.mesh.vertex_attributes(v, 'xy') + [0]
            lines.append({'start': start, 'end': end, 'name': "FormDiagram.edge", 'color': color[key]})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text, color):
        labels = []
        for key in text:
            u, v = key
            a = self.mesh.vertex_attributes(u, 'xy') + [0]
            b = self.mesh.vertex_attributes(v, 'xy') + [0]
            pos = [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.0]
            labels.append({'pos': pos, 'text': text[key], 'name': "FormDiagram.edgelabel", 'color': color[key]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
