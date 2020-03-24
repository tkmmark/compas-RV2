from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import color_to_colordict
from compas_rv2.rhino.artists.meshartist import MeshArtist


__all__ = ['FormArtist']


class FormArtist(MeshArtist):

    def draw_vertices(self, keys, color):
        points = []
        for key in keys:
            xy = self.mesh.vertex_attributes(key, 'xy')
            points.append({'pos': xy + [0], 'name': "FormDiagram.vertex", 'color': color[key]})
        return compas_rhino.draw_points(points, layer=self.settings['form.layer'], clear=False, redraw=False)

    def draw_edges(self, keys, color):
        lines = []
        for key in keys:
            u, v = key
            start = self.mesh.vertex_attributes(u, 'xy') + [0]
            end = self.mesh.vertex_attributes(v, 'xy') + [0]
            lines.append({'start': start, 'end': end, 'name': "FormDiagram.edge", 'color': color[key]})
        return compas_rhino.draw_lines(lines, layer=self.settings['form.layer'], clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
