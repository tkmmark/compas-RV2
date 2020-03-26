from math import radians
from math import pi

from compas.geometry import Polygon
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import centroid_points_xy
from compas.datastructures import Mesh
from compas.utilities import pairwise
from compas.utilities import flatten
from compas_plotters import MeshPlotter

from triangle import triangulate

# ==============================================================================
# Boundaries
# ==============================================================================

outer = Polygon.from_sides_and_radius_xy(4, 1.0)
inner = Polygon.from_sides_and_radius_xy(4, 0.25)

inner.transform(Rotation.from_axis_and_angle([0, 0, 1], radians(45)))

outer_xy = [[x, y] for x, y, z in outer.points]
inner_xy = [[x, y] for x, y, z in inner.points]

# ==============================================================================
# Input data
# ==============================================================================

o = len(outer_xy)
i = o + len(inner_xy)

outer_segments = list(pairwise(range(o))) + [(o - 1, 0)]
inner_segments = list(pairwise(range(o, i))) + [(i - 1, o)]

vertices = outer_xy + inner_xy
segments = outer_segments + inner_segments
point = centroid_points_xy(inner_xy)
holes = [point[:2]]

# ==============================================================================
# Remesh polygon boundaries
# ==============================================================================

tri = {'vertices': vertices, 'segments': segments, 'holes': holes}
tri = triangulate(tri, opts='p')
tri = triangulate(tri, opts='pra0.0005q')

vertices = [[x, y, 0] for x, y in tri['vertices']]
triangles = tri['triangles'].tolist()

mesh = Mesh.from_vertices_and_faces(vertices, triangles)

# ==============================================================================
# Visualization
# ==============================================================================

# plotter = MeshPlotter(mesh, figsize=(8, 5))

# plotter.draw_faces()
# plotter.show()
