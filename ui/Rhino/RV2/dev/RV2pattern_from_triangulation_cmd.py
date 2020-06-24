from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.utilities import geometric_key
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas_rhino.geometry import RhinoCurve
from compas_rv2.datastructures import Pattern

import rhinoscriptsyntax as rs


__commandname__ = "RV2pattern_from_triangulation"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    conforming_delaunay_triangulation = proxy.function('compas_triangle.delaunay.conforming_delaunay_triangulation')

    boundary_guids = compas_rhino.select_curves('Select outer boundary.')
    if not boundary_guids:
        return

    hole_guids = compas_rhino.select_curves('Select inner boundaries.')
    segments_guids = compas_rhino.select_curves('Select constraint curves.')

    target_length = rs.GetReal('Specifiy target edge length.')
    if not target_length:
        return

    gkey_constraints = {}

    # outer boundary
    boundary = []
    for guid in boundary_guids:
        compas_rhino.rs.EnableRedraw(False)
        segments = compas_rhino.rs.ExplodeCurves(guid)
        for segment in segments:
            curve = RhinoCurve.from_guid(segment)
            N = max(int(curve.length() / target_length), 1)
            points = map(list, curve.divide(N, over_space=True))
            for point in points:
                gkey = geometric_key(point)
                if gkey not in gkey_constraints:
                    gkey_constraints[gkey] = []
                gkey_constraints[gkey].append(segment)
            boundary.extend(points)
        # for segment in segments:
        #     compas_rhino.rs.ObjectLayer(segment, "RV2::Constraints::Boundary")
        compas_rhino.delete_objects(segments, purge=True)
        compas_rhino.rs.EnableRedraw(True)

    # constraint polylines
    polylines = []
    if segments_guids:
        for guid in segments_guids:
            curve = RhinoCurve.from_guid(guid)
            N = int(curve.length() / target_length) or 1
            points = map(list, curve.divide(N, over_space=True))
            for point in points:
                gkey = geometric_key(point)
                if gkey not in gkey_constraints:
                    gkey_constraints[gkey] = []
                gkey_constraints[gkey].append(guid)
            polylines.append(points)
            # compas_rhino.rs.ObjectLayer(guid, "RV2::Constraints::Curves")

    # hole polygons
    on_hole = []
    polygons = []
    if hole_guids:
        for guid in hole_guids:
            curve = RhinoCurve.from_guid(guid)
            N = int(curve.length() / target_length) or 1
            points = map(list, curve.divide(N, over_space=True))
            for point in points:
                gkey = geometric_key(point)
                if gkey not in gkey_constraints:
                    gkey_constraints[gkey] = []
                gkey_constraints[gkey].append(guid)
                on_hole.append(gkey)
            polygons.append(points)
            # compas_rhino.rs.ObjectLayer(guid, "RV2::Constraints::Holes")

    area = target_length ** 2 * 0.5 * 0.5 * 1.732

    vertices, faces = conforming_delaunay_triangulation(boundary, polylines=polylines, polygons=polygons, angle=30, area=area)
    vertices[:] = [[float(x), float(y), float(z)] for x, y, z in vertices]

    pattern = Pattern.from_vertices_and_faces(vertices, faces)

    # vertices on constraints should store a reference to the constraint
    # vertices with more than one constraint are corners and should be marked as anchor/fixed

    gkey_key = {geometric_key(pattern.vertex_coordinates(key)): key for key in pattern.vertices()}

    for gkey in gkey_constraints:
        guids = gkey_constraints[gkey]
        if gkey in gkey_key:
            key = gkey_key[gkey]
            if len(guids) > 1:
                pattern.vertex_attribute(key, 'is_fixed', True)
            pattern.vertex_attribute(key, 'constraint', [str(guid) for guid in guids])
            if gkey in on_hole:
                pattern.vertex_attribute(key, 'is_fixed', True)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    print('Pattern object successfully created.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
