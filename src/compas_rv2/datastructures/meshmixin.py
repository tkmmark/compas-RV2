from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from compas.utilities import pairwise


__all__ = ['MeshMixin']


class MeshMixin(object):
    """Mixin for all mesh-based data structure in RV2."""

    def edge_loop(self, uv):
        if self.is_edge_on_boundary(*uv):
            return self._edge_loop_on_boundary(uv)

        edges = []
        current, previous = uv
        edges.append((previous, current))

        while True:
            if current == uv[1]:
                break
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))

        edges[:] = [(u, v) for v, u in edges[::-1]]

        if edges[0][0] == edges[-1][1]:
            return edges

        previous, current = uv
        while True:
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))

        return edges

    def _edge_loop_on_boundary(self, uv):
        edges = []
        current, previous = uv
        edges.append((previous, current))

        while True:
            if current == uv[1]:
                break
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))

        edges[:] = [(u, v) for v, u in edges[::-1]]

        if edges[0][0] == edges[-1][1]:
            return edges

        previous, current = uv
        while True:
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))

        return edges

    def edge_strip(self, uv):
        edges = []
        v, u = uv
        while True:
            edges.append((u, v))
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        edges[:] = [(u, v) for v, u in edges[::-1]]
        u, v = uv
        while True:
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
            edges.append((u, v))
        return edges

    def vertices_on_edge_loop(self, uv):
        edges = self.edge_loop(uv)
        if len(edges) == 1:
            return edges[0]
        vertices = [edge[0] for edge in edges]
        if edges[-1][1] != edges[0][0]:
            vertices.append(edges[-1][1])
        return vertices

    # def faces_on_edge_loop(self, uv):
    #     pass

    # def faces_on_edge_strip(self, uv):
    #     pass

    # def continuous_vertices_on_boundary(self, uv):
    #     vertices = []
    #     current, previous = uv
    #     vertices.append(current)
    #     if not self.vertex_attribute(current, 'is_fixed'):
    #         while True:
    #             nbrs = self.vertex_neighbors(current)
    #             for nbr in nbrs:
    #                 if nbr == previous:
    #                     continue
    #                 if self.is_edge_on_boundary(current, nbr):
    #                     vertices.append(nbr)
    #                     break
    #             if vertices[-1] == vertices[0]:
    #                 break
    #             if self.vertex_attribute(vertices[-1], 'is_fixed'):
    #                 break
    #             previous = current
    #             current = nbr
    #         vertices[:] = vertices[::-1]
    #     previous, current = uv
    #     vertices.append(current)
    #     if not self.vertex_attribute(current, 'is_fixed'):
    #         while True:
    #             nbrs = self.vertex_neighbors(current)
    #             for nbr in nbrs:
    #                 if nbr == previous:
    #                     continue
    #                 if self.is_edge_on_boundary(current, nbr):
    #                     vertices.append(nbr)
    #                     break
    #             if vertices[-1] == vertices[0]:
    #                 break
    #             if self.vertex_attribute(vertices[-1], 'is_fixed'):
    #                 break
    #             previous = current
    #             current = nbr
    #     return vertices

    # def continuous_vertices(self, uv):
    #     """Ordered vertices along the direction of an edge.

    #     Note that the direction of an edge only makes sense in a quad patch
    #     of the diagram. Therefore, the search in either direction of the edge
    #     stops if the next encountered vertex is not 4-valent, or if it is on
    #     the boundary of the diagram.

    #     Parameters
    #     ----------
    #     uv : tuple
    #         The edge identifier.

    #     Returns
    #     -------
    #     list
    #         Ordered vertices along the direction of the edge.
    #         The first vertex is the vertex at the end of the u-direction.
    #         The last vertex is the vertex at the end of the v-direction.

    #     """
    #     valency = 4
    #     if self.is_edge_on_boundary(*uv):
    #         valency = 3

    #     vertices = []
    #     current, previous = uv
    #     while True:
    #         vertices.append(current)
    #         nbrs = self.vertex_neighbors(current, ordered=True)
    #         if len(nbrs) != valency:
    #             break
    #         i = nbrs.index(previous)
    #         previous = current
    #         current = nbrs[i - 2]
    #         if valency == 3 and not self.is_edge_on_boundary(previous, current):
    #             current = nbrs[i - 1]

    #     vertices[:] = vertices[::-1]

    #     previous, current = uv

    #     while True:
    #         vertices.append(current)
    #         nbrs = self.vertex_neighbors(current, ordered=True)
    #         if len(nbrs) != valency:
    #             break
    #         i = nbrs.index(previous)
    #         previous = current
    #         current = nbrs[i - 2]
    #         if valency == 3 and not self.is_edge_on_boundary(previous, current):
    #             current = nbrs[i - 1]

    #     return vertices

    # def continuous_edges(self, uv):
    #     """Ordered edges along the direction of an edge.

    #     Note that the direction of an edge only makes sense in a quadpatch
    #     of the diagram. Therefore, the search in either direction of the edges
    #     stops if the opposite vertex of the next encountered edge is not
    #     4-valent or if it lies on the boundary of the diagram.

    #     Parameters
    #     ----------
    #     uv : tuple
    #         The edge identifier.

    #     Returns
    #     -------
    #     list
    #         A list of ordered edge identifiers.
    #         Edges are aligned head-to-tail.
    #         Therefore, the orientation of the edges is not necessarily the same as in the diagram.
    #         The first edge is the edge at the end of the u-direction.
    #         The last edge is the edge at the end of the

    #     """
    #     vertices = self.continuous_vertices(uv)
    #     return list(pairwise(vertices))

    # def parallel_edges(self, uv):
    #     """Edges parallel to an edge.

    #     Parallel edges only exist in a quadpatch of the diagram.
    #     The search in either direction stops as soon as the next edge
    #     is adjacent to a face that is not a quadrilateral or if it is on
    #     the boundary of the diagram.

    #     Parameters
    #     ----------
    #     uv : tuple
    #         The edge identifier.

    #     Returns
    #     -------
    #     list
    #         A list of parallel edges.

    #     """
    #     edges = []
    #     v, u = uv
    #     while True:
    #         fkey = self.halfedge[u][v]
    #         if fkey is None:
    #             break
    #         vertices = self.face_vertices(fkey)
    #         if len(vertices) != 4:
    #             break
    #         edges.append((u, v))
    #         i = vertices.index(u)
    #         u = vertices[i - 1]
    #         v = vertices[i - 2]
    #     edges[:] = edges[::-1]
    #     u, v = uv
    #     while True:
    #         fkey = self.halfedge[u][v]
    #         if fkey is None:
    #             break
    #         vertices = self.face_vertices(fkey)
    #         if len(vertices) != 4:
    #             break
    #         edges.append((u, v))
    #         i = vertices.index(u)
    #         u = vertices[i - 1]
    #         v = vertices[i - 2]
    #     return edges

    # def parallel_faces(self, uv):
    #     """The faces along the direction of parallel edges.

    #     Parameters
    #     ----------
    #     uv : tuple
    #         The edge identifier.

    #     Returns
    #     -------
    #     list
    #         A list of parallel faces.

    #     """
    #     faces = []
    #     v, u = uv
    #     while True:
    #         fkey = self.halfedge[u][v]
    #         if fkey is None:
    #             break
    #         vertices = self.face_vertices(fkey)
    #         if len(vertices) != 4:
    #             break
    #         faces.append(fkey)
    #         i = vertices.index(u)
    #         u = vertices[i - 1]
    #         v = vertices[i - 2]
    #     faces[:] = faces[::-1]
    #     u, v = uv
    #     while True:
    #         fkey = self.halfedge[u][v]
    #         if fkey is None:
    #             break
    #         vertices = self.face_vertices(fkey)
    #         if len(vertices) != 4:
    #             break
    #         faces.append(fkey)
    #         i = vertices.index(u)
    #         u = vertices[i - 1]
    #         v = vertices[i - 2]
    #     return faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
