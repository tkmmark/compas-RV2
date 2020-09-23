from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

import compas_rhino
from compas_rhino.artists._artist import BaseArtist

from compas.utilities import color_to_colordict


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ["SkeletonArtist"]


class SkeletonArtist(BaseArtist):
    """Artist for the visualisation of Skeleton data structures."""

    def __init__(self, skeleton, layer=None):
        super(SkeletonArtist, self).__init__()
        self._skeleton = None
        self._vertex_xyz = None
        self.skeleton = skeleton
        self.layer = layer
        self.color_vertices = (255, 0, 0)
        self.color_edges = (0, 0, 255)
        self.color_mesh_vertices = (0, 0, 0)
        self.color_mesh_edges = (0, 0, 0)

    @property
    def skeleton(self):
        return self._skeleton

    @skeleton.setter
    def skeleton(self, skeleton):
        self._skeleton = skeleton
        self._vertex_xyz = None

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.skeleton.vertex_attributes(vertex, 'xyz') for vertex in self.skeleton.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated skeleton."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.skeleton.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw the skeleton vertices and branches and the resulting (dense) mesh."""
        pass

    # ==========================================================================
    # The skeleton
    # ==========================================================================

    def draw_skeleton_vertices(self, vertices=None, color=None):
        """Draw the skeleton vertices."""
        vertices = vertices or list(self.skeleton.skeleton_vertices[0] + self.skeleton.skeleton_vertices[1])
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertices, default=self.color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.skeleton.name, vertex),
                'color': vertex_color[vertex]})
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_skeleton_edges(self, edges=None, color=None):
        """Draw the skeleton edges."""
        edges = edges or list(self.skeleton.skeleton_branches)
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.skeleton.name, *edge)})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # The coarse mesh
    # ==========================================================================

    def draw_mesh_vertices(self, vertices=None, color=None):
        """Draw the vertices of the coarse mesh."""
        mesh_vertices = set(self.skeleton.vertices())
        skeleton_vertices = set(self.skeleton.skeleton_vertices[0] + self.skeleton.skeleton_vertices[1])
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertices, default=self.color_mesh_vertices)
        vertices = vertices or list(mesh_vertices - skeleton_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.skeleton.name, vertex),
                'color': vertex_color[vertex]})
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_mesh_edges(self, edges=None, color=None):
        """Draw the edges of the coarse mesh."""
        pass
