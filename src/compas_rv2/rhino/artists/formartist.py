from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import color_to_colordict
from compas_rv2.rhino.artists.meshartist import MeshArtist


__all__ = ['FormArtist']


class FormArtist(MeshArtist):

    def draw_vertices(self, keys, color):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
        color : dict
            The color specififcation for the vertices as key-color pairs.
            Each color should be a list of RGB components.

        """
        points = []
        for key in keys:
            points.append({
                'pos': self.mesh.vertex_attributes(key, 'xy') + [0],
                'name': "{}.vertex.{}".format(self.mesh.name, key),
                'color': colordict[key],
                'layer': self.mesh.vertex_attribute(key, 'layer')
            })
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_edges(self, keys, color):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
        color : dict
            The color specififcation for the vertices as key-color pairs.
            Each color should be a list of RGB components.

        """
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.mesh.vertex_attributes(u, 'xy') + [0],
                'end': self.mesh.vertex_attributes(v, 'xy') + [0],
                'color': color[(u, v)],
                'name': "{}.edge.{}-{}".format(self.mesh.name, u, v),
                'layer': self.mesh.edge_attribute((u, v), 'layer')
            })
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
