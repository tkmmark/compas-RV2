from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
from compas_tna.diagrams import ForceDiagram as _ForceDiagram


__all__ = ['ForceDiagram']


class ForceDiagram(_ForceDiagram):

    def continuous_vertices(self, uv):
        vertices = []
        current, previous = uv
        while True:
            vertices.append(current)
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
        vertices[:] = vertices[::-1]
        previous, current = uv
        while True:
            vertices.append(current)
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
        return vertices

    def continuous_edges(self, uv):
        vertices = self.continuous_vertices(uv)
        return list(pairwise(vertices))

    def parallel_edges(self, uv):
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
