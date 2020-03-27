from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas_rhino.geometry import RhinoCurve
from compas_rv2.datastructures import Pattern
from compas.geometry import centroid_points_xy
from compas.utilities import geometric_key
from compas.utilities import pairwise
import rhinoscriptsyntax as rs
import math

from compas.rpc import Proxy

igl = Proxy('compas_libigl')

__commandname__ = "RV2pattern_from_triangulation"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    boundary_guids = compas_rhino.select_curves('select outer boundary')
    if not boundary_guids:
        return

    hole_guids = compas_rhino.select_curves('select inner boundary')
    segments_guids = compas_rhino.select_curves('select guide line')
    target_length = rs.GetReal('target edge length')
    if not target_length:
        return

    # boundary
    boundary = RhinoCurve.from_guid(boundary_guids[0])
    divide = math.floor(boundary.length()/target_length)
    points = boundary.divide(divide, over_space=True)
    boundary = points

    # hole
    hole = []
    if hole_guids:
        hole = RhinoCurve.from_guid(hole_guids[0])
        divide = math.floor(hole.length()/target_length)
        points = hole.divide(divide, over_space=True)
        hole = points

    # segments
    segments = []
    if segments_guids:
        segments = RhinoCurve.from_guid(segments_guids[0])
        divide = math.floor(segments.length()/target_length)
        points = segments.divide(divide, over_space=True)
        segments = points

    # data
    data = {
        "boundary": boundary,
        "segments": segments,
        "hole": hole,
        "target_length": target_length
    }

    gkey_xyz = {geometric_key(point): point for point in data['boundary']}
    gkey_xyz.update({geometric_key(point): point for point in data['segments']})
    gkey_xyz.update({geometric_key(point): point for point in data['hole']})
    gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz.keys())}

    xyz = list(gkey_xyz.values())
    edges = []
    edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['boundary'])]
    edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['segments'])]
    edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['hole'])]

    if data['hole']:
        holes = []
        holes += [centroid_points_xy([xyz[gkey_index[geometric_key(point)]] for point in data['hole'][:-1]])]
    else:
        holes = None

    area = data['target_length'] ** 2 * 0.5 * 0.5 * 1.732
    V2, F2 = igl.conforming_delaunay_triangulation(xyz, edges, holes, area=area)

    pattern = Pattern.from_vertices_and_faces(V2, F2)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
