from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise


__all__ = ['MeshMixin']


class MeshMixin(object):
    """Mixin for all mesh-based data structure in RV2."""

    def continuous_vertices_on_boundary(self, uv):
        vertices = []
        current, previous = uv
        vertices.append(current)
        if not self.vertex_attribute(current, 'is_fixed'):
            while True:
                nbrs = self.vertex_neighbors(current)
                for nbr in nbrs:
                    if nbr == previous:
                        continue
                    if self.is_edge_on_boundary(current, nbr):
                        vertices.append(nbr)
                        break
                if vertices[-1] == vertices[0]:
                    break
                if self.vertex_attribute(vertices[-1], 'is_fixed'):
                    break
                previous = current
                current = nbr
            vertices[:] = vertices[::-1]
        previous, current = uv
        vertices.append(current)
        if not self.vertex_attribute(current, 'is_fixed'):
            while True:
                nbrs = self.vertex_neighbors(current)
                for nbr in nbrs:
                    if nbr == previous:
                        continue
                    if self.is_edge_on_boundary(current, nbr):
                        vertices.append(nbr)
                        break
                if vertices[-1] == vertices[0]:
                    break
                if self.vertex_attribute(vertices[-1], 'is_fixed'):
                    break
                previous = current
                current = nbr
        return vertices

    def continuous_vertices(self, uv):
        """Ordered vertices along the direction of an edge.

        Note that the direction of an edge only makes sense in a quad patch
        of the diagram. Therefore, the search in either direction of the edge
        stops if the next encountered vertex is not 4-valent, or if it is on
        the boundary of the diagram.

        Parameters
        ----------
        uv : tuple
            The edge identifier.

        Returns
        -------
        list
            Ordered vertices along the direction of the edge.
            The first vertex is the vertex at the end of the u-direction.
            The last vertex is the vertex at the end of the v-direction.

        """
        valency = 4
        if self.is_edge_on_boundary(*uv):
            valency = 3

        vertices = []
        current, previous = uv
        while True:
            vertices.append(current)
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != valency:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            if valency == 3 and not self.is_edge_on_boundary(previous, current):
                current = nbrs[i - 1]

        vertices[:] = vertices[::-1]

        previous, current = uv

        while True:
            vertices.append(current)
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != valency:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            if valency == 3 and not self.is_edge_on_boundary(previous, current):
                current = nbrs[i - 1]

        return vertices

    def continuous_edges(self, uv):
        """Ordered edges along the direction of an edge.

        Note that the direction of an edge only makes sense in a quadpatch
        of the diagram. Therefore, the search in either direction of the edges
        stops if the opposite vertex of the next encountered edge is not
        4-valent or if it lies on the boundary of the diagram.

        Parameters
        ----------
        uv : tuple
            The edge identifier.

        Returns
        -------
        list
            A list of ordered edge identifiers.
            Edges are aligned head-to-tail.
            Therefore, the orientation of the edges is not necessarily the same as in the diagram.
            The first edge is the edge at the end of the u-direction.
            The last edge is the edge at the end of the

        """
        vertices = self.continuous_vertices(uv)
        return list(pairwise(vertices))

    def parallel_edges(self, uv):
        """Edges parallel to an edge.

        Parallel edges only exist in a quadpatch of the diagram.
        The search in either direction stops as soon as the next edge
        is adjacent to a face that is not a quadrilateral or if it is on
        the boundary of the diagram.

        Parameters
        ----------
        uv : tuple
            The edge identifier.

        Returns
        -------
        list
            A list of parallel edges.

        """
        edges = []
        v, u = uv
        while True:
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            edges.append((u, v))
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        edges[:] = edges[::-1]
        u, v = uv
        while True:
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            edges.append((u, v))
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        return edges

    def parallel_faces(self, uv):
        """The faces along the direction of parallel edges.

        Parameters
        ----------
        uv : tuple
            The edge identifier.

        Returns
        -------
        list
            A list of parallel faces.

        """
        faces = []
        v, u = uv
        while True:
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            faces.append(fkey)
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        faces[:] = faces[::-1]
        u, v = uv
        while True:
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            faces.append(fkey)
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        return faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
