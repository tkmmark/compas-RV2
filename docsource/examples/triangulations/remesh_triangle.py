from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from triangle import triangulate
except ImportError:
    pass

from compas.utilities import pairwise
from compas.utilities import flatten
from compas.geometry import centroid_points_xy


__all__ = ['remesh_triangle']


def remesh_triangle(vertices, target, boundary=None):
    vertices = [vertex[:2] for vertex in vertices]

    if boundary:
        data = {'vertices': vertices, 'segments': boundary}
        result = triangulate(data, opts='pa{}q'.format(target))

    else:
        data = {'vertices': vertices}
        result = triangulate(data, opts='a{}q'.format(target))

    vertices = [[x, y, 0] for x, y in result['vertices']]
    triangles = result['triangles'].tolist()

    return vertices, triangles


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Polygon
    from compas.datastructures import Mesh
    from compas.utilities import pairwise
    from compas_plotters import MeshPlotter

    points = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (6.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
    polygon = Polygon(points)

    p = len(points)

    area = polygon.area
    boundary = list(pairwise(range(p))) + [(p - 1, 0)]

    vertices, faces = remesh_triangle(polygon.points, area/500, boundary=boundary)

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    plotter = MeshPlotter(mesh, figsize=(8, 5))
    plotter.draw_faces()
    plotter.show()
