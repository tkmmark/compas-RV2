from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.utilities import color_to_colordict
from compas_rhino.artists import MeshArtist


__all__ = ['ThrustArtist']


class ThrustArtist(MeshArtist):

    def draw_external(self, scale=1.0):
        lines = []
        for key in self.mesh.vertices_where({'is_anchor': True}):
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector([0, 0, r[2]], scale))
            lines.append({
                'start': a,
                'end': b,
                'color': (0, 255, 255),
                'arrow': "start"
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_residual(self, scale=1.0):
        lines = []
        for key in self.mesh.vertices_where({'is_anchor': False, 'is_external': False}):
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector([0, 0, r[2]], scale))
            lines.append({
                'start': a,
                'end': b,
                'color': (0, 255, 255),
                'arrow': "start"
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
