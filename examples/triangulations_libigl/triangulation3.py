import os
import json
# import numpy
import compas
from compas.datastructures import Mesh
from compas.geometry import centroid_points_xy
from compas_plotters import MeshPlotter
from compas.utilities import geometric_key
from compas.utilities import pairwise
# from compas.rpc import Proxy
# # import compas_libigl as igl
# igl = Proxy('compas_libigl')

from triangle import triangulate


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE = os.path.join(DATA, 'rhino1.json')

with open(FILE, 'r') as f:
    data = json.load(f)

gkey_xyz = {geometric_key(point): point for point in data['boundary']}
gkey_xyz.update({geometric_key(point): point for point in data['segments']})
gkey_xyz.update({geometric_key(point): point for point in data['hole']})
gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz.keys())}

xyz = list(gkey_xyz.values())
edges = []
edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['boundary'])]
edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['segments'])]
edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['hole'])]
holes = []
holes += [centroid_points_xy([xyz[gkey_index[geometric_key(point)]] for point in data['hole'][:-1]])[:2]]

# V2, F2 = igl.delaunay_triangulation(V)
# V2, F2 = igl.constrained_delaunay_triangulation(V, E)
# V2, F2 = igl.conforming_delaunay_triangulation(xyz, edges, holes, area=0.05)

xy = [[x, y] for x, y, _ in xyz]

tri = {'vertices': xy, 'segments': edges, 'holes': holes}
tri = triangulate(tri, opts='pa0.05q')

V2 = [[x, y, 0] for x, y in tri['vertices']]
F2 = tri['triangles'].tolist()

mesh = Mesh.from_vertices_and_faces(V2, F2)

lines = []
for u, v in edges:
    lines.append({'start': xyz[u], 'end': xyz[v], 'color': '#ff0000', 'width': 2.0})

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
