from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas_rv2.datastructures import Pattern
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import centroid_points_xy
from compas.utilities import pairwise
from compas.utilities import flatten
import rhinoscriptsyntax as rs


__commandname__ = "RV2pattern_from_triangulation"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    p = get_proxy()
    if not p:
        return

        raise NotImplementedError

    # triangulate = p.package("triangle.triangulate")

    # # ==============================================================================
    # # Boundaries from Rhino
    # # ==============================================================================

    # outer_guid = compas_rhino.select_curve('select outer boundary curve')
    # inner_guids = compas_rhino.select_curves('select inner boundary curves')
    # guide_guids = compas_rhino.select_curves('select guide lines')
    # target_length = rs.GetReal('target edge length')

    # if not outer_guid:
    #     return
    # if not target_length:
    #     return

    # # outer
    # outer_guids = rs.ExplodeCurves(outer_guid, False)
    # outer = []
    # for guid in outer_guids:
    #     pts = rs.DivideCurve(guid, rs.CurveLength(guid) / target_length)[:-1]
    #     outer.extend(pts)
    # outer = Polygon(outer)
    # compas_rhino.delete_objects(outer_guids)

    # # inner
    # inners = []
    # holes = []
    # for guid in inner_guids:
    #     pts = rs.DivideCurve(guid, rs.CurveLength(guid) / target_length)
    #     inners.append(Polygon(pts))
    #     holes.append(centroid_points_xy(pts))

    # # guide
    # guides = []
    # for guid in guide_guids:
    #     pts = rs.DivideCurve(guid, rs.CurveLength(guid) / target_length)
    #     guides.append(Polyline(pts))

    # # ==============================================================================
    # # Input data
    # # ==============================================================================

    # boundaries = [outer] + inners

    # vertices = list(flatten(boundaries + guides))
    # vertices = [[x, y] for x, y, z in vertices]
    # holes = [[x, y] for x, y, z in holes]

    # segments = []
    # index = 0
    # for polygon in boundaries:
    #     start = index
    #     end = start + len(polygon)
    #     segments.extend(list(pairwise(range(start, end))) + [(end - 1, start)])
    #     index = end

    # if guides:
    #     for polyline in guides:
    #         start = index
    #         end = start + len(polyline)
    #         segments.extend(list(pairwise(range(start, end))))
    #         index = end

    # area_constrain = target_length ** 2 * 0.5 * 0.5 * 1.732  # calculate a triangle area based on target edge length # noqa E501

    # if not inners:  # no inner boundary
    #     tri = {'vertices': vertices, 'segments': segments}
    #     tri = triangulate(tri, opts='pa{}q'.format(area_constrain))
    # else:
    #     tri = {'vertices': vertices, 'segments': segments, 'holes': holes}
    #     tri = triangulate(tri, opts='p')
    #     tri = triangulate(tri, opts='ra{}q'.format(area_constrain))  # this doesn't take fixed segements from previous step # noqa 501

    # vertices = [[x, y, 0] for x, y in tri['vertices']]
    # triangles = list(tri['triangles'])

    # pattern = Pattern.from_vertices_and_faces(vertices, triangles)

    # scene.clear()
    # scene.add(pattern, name='pattern')
    # scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
