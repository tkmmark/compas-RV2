from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino

from compas_rhino.artists._artist import BaseArtist

from compas.utilities import color_to_colordict
from compas.utilities import pairwise
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_polygon
from compas.geometry import centroid_points


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ["SkeletonArtist"]


class SkeletonArtist(BaseArtist):
    """Artist for the visualisation of Skeleton data structures."""

    def __init__(self, skeleton, layer=None):
        super(SkeletonArtist, self).__init__()
        self._skeleton = None
        self._mesh = None
        self._skeleton_vertex_xyz = None
        self._mesh_vertex_xyz = None
        self.skeleton = skeleton
        self.layer = layer
        self.skeleton_color_vertices = (255, 0, 0)
        self.skeleton_color_edges = (0, 0, 255)
        self.mesh_color_vertices = (0, 0, 0)
        self.mesh_color_edges = (0, 0, 0)
        self.mesh_color_faces = (0, 0, 0)

    @property
    def skeleton(self):
        return self._skeleton

    @skeleton.setter
    def skeleton(self, skeleton):
        self._skeleton = skeleton
        self._mesh = None
        self._skeleton_vertex_xyz = None
        self._mesh_vertex_xyz = None

    @property
    def mesh(self):
        if not self._mesh:
            self._mesh = self.skeleton.to_mesh()
        return self._mesh

    @property
    def skeleton_vertex_xyz(self):
        if not self._skeleton_vertex_xyz:
            self._skeleton_vertex_xyz = {vertex: self.skeleton.vertex_attributes(vertex, 'xyz') for vertex in self.skeleton.vertices()}
        return self._skeleton_vertex_xyz

    @skeleton_vertex_xyz.setter
    def skeleton_vertex_xyz(self, vertex_xyz):
        self._skeleton_vertex_xyz = vertex_xyz

    @property
    def mesh_vertex_xyz(self):
        if not self._mesh_vertex_xyz:
            self._mesh_vertex_xyz = {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._mesh_vertex_xyz

    @mesh_vertex_xyz.setter
    def mesh_vertex_xyz(self, vertex_xyz):
        self._mesh_vertex_xyz = vertex_xyz

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

    def draw_skeleton_vertices(self, vertices=None, color=None):
        """Draw the skeleton vertices."""
        vertices = vertices or list(self.skeleton.skeleton_vertices[0] + self.skeleton.skeleton_vertices[1])
        vertex_xyz = self.skeleton_vertex_xyz
        vertex_color = colordict(color, vertices, default=self.skeleton_color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.skeleton.name, vertex),
                'color': vertex_color[vertex]})
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_skeleton_edges(self, edges=None, color=None):
        """Draw the skeleton edges."""
        pass

    def draw_coarse_mesh_vertices(self, vertices=None, color=None):
        """Draw the vertices of the coarse mesh."""
        pass

    def draw_coarse_mesh_edges(self, edges=None, color=None):
        """Draw the edges of the coarse mesh."""
        pass

    def draw_mesh(self, disjoint=True):
        """Draw the resulting mesh."""
        pass

    def draw_mesh_vertices(self, vertices=None, color=None):
        """Draw the vertices of the resulting mesh."""
        pass

    def draw_mesh_edges(self, edges=None, color=None):
        """Draw the edges of the resulting mesh."""
        pass

    def draw_mesh_faces(self, faces=None, color=None):
        """Draw the faces of the resulting mesh."""
        pass
