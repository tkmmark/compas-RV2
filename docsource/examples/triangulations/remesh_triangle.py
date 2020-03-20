from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from triangle import triangulate
except ImportError:
    pass

from compas.utilities import pairwise
from compas.geometry import centroid_points_xy


__all__ = ['trimesh_remesh_triangle']


def trimesh_remesh_triangle(mesh, target, segments=None):
    tri = {
        'vertices': list(mesh.vertices_attributes('xy')),
        'segments': segments,
    }
    result = triangulate(tri, opts='pa{}q'.format(target))
    vertices = [[x, y, 0] for x, y in result['vertices']]
    triangles = result['triangles'].tolist()
    cls = type(mesh)
    return cls.from_vertices_and_faces(vertices, triangles)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh
    from compas_plotters import MeshPlotter

    vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (6.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
    faces = [[0, 1, 2, 3]]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    key = mesh.insert_vertex(0)

    area = sum(mesh.face_area(fkey) for fkey in mesh.faces()) / mesh.number_of_faces()
    segments = list(mesh.edges())

    finer = trimesh_remesh_triangle(mesh, area/200, segments=segments)

    plotter = MeshPlotter(finer, figsize=(8, 5))
    plotter.draw_edges()
    plotter.show()
