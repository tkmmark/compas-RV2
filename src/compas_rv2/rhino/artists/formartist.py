from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import color_to_colordict
from compas_rhino.artists import MeshArtist


__all__ = ['FormArtist']


class FormArtist(MeshArtist):

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default vertex
            color (``self.settings['color.vertex']``).
            The default is ``None``, in which case all vertices are assigned the
            default vertex color.

        Notes
        -----
        The vertices are named using the following template:
        ``"{}.vertex.{}".format(self.mesh.name, key)``.
        This name is used afterwards to identify vertices in the Rhino model.

        """
        keys = keys or list(self.mesh.vertices())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for key in keys:
            points.append({
                'pos': self.mesh.vertex_attributes(key, 'xy') + [0],
                'name': "{}.vertex.{}".format(self.mesh.name, key),
                'color': colordict[key],
                'layer': self.mesh.vertex_attribute(key, 'layer')
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all edges, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All edges are named using the following template:
        ``"{}.edge.{}-{}".fromat(self.mesh.name, u, v)``.
        This name is used afterwards to identify edges in the Rhino model.
        """
        keys = keys or list(self.mesh.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.mesh.vertex_attributes(u, 'xy') + [0],
                'end': self.mesh.vertex_attributes(v, 'xy') + [0],
                'color': colordict[(u, v)],
                'name': "{}.edge.{}-{}".format(self.mesh.name, u, v),
                'layer': self.mesh.edge_attribute((u, v), 'layer')
            })

        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
