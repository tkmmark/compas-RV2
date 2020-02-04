from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import color_to_colordict

from compas_rhino.artists import MeshArtist
from compas_rv2.rhino import RhinoDiagram


__all__ = ["RhinoFormDiagram"]


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


class RhinoFormDiagram(RhinoDiagram):

    def __init__(self, diagram):
        super(RhinoFormDiagram, self).__init__(diagram)
        self.artist = FormArtist(self.diagram)

        self.vertex_attribute_editable('is_anchor', True)
        self.vertex_attribute_editable('x', True)
        self.vertex_attribute_editable('y', True)
        self.vertex_attribute_editable('z', True)

    def draw(self, settings):
        self.artist.layer = settings.get("layers.form")
        self.artist.clear_layer()

        if settings.get("show.form.vertices", True):
            color = {}
            color.update({key: settings.get("color.form.vertices") for key in self.diagram.vertices()})
            color.update({key: settings.get("color.form.vertices:is_fixed") for key in self.diagram.vertices_where({'is_fixed': True})})
            color.update({key: settings.get("color.form.vertices:is_external") for key in self.diagram.vertices_where({'is_external': True})})
            color.update({key: settings.get("color.form.vertices:is_anchor") for key in self.diagram.vertices_where({'is_anchor': True})})
            self.guid_vertices = self.artist.draw_vertices(color=color)

        if settings.get("show.form.edges", True):
            keys = list(self.diagram.edges_where({'is_edge': True}))
            color = {}
            color = {}
            for key in keys:
                u, v = key
                if self.diagram.vertex_attribute(u, 'is_external') or self.diagram.vertex_attribute(v, 'is_external'):
                    color[key] = settings.get("color.form.edges:is_external")
                else:
                    color[key] = settings.get("color.form.edges")
            self.guid_edges = self.artist.draw_edges(keys=keys, color=color)

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
