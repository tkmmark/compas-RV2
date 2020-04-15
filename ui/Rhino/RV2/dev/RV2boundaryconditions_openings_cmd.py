from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.utilities import pairwise
from compas.geometry import centroid_points
from compas.geometry import distance_point_point_xy
from compas.geometry import intersection_line_line_xy
from compas.geometry import midpoint_point_point_xy

__commandname__ = "RV2boundaryconditions_openings"


def relax_pattern(pattern, relax):
    key_index = pattern.key_index()
    xyz = pattern.vertices_attributes('xyz')
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed = [key_index[key] for key in pattern.vertices_where({'is_anchor': True})]
    edges = [(key_index[u], key_index[v]) for u, v in pattern.edges()]
    q = list(pattern.edges_attribute('q'))
    xyz, q, f, l, r = relax(xyz, edges, fixed, q, loads)
    for key in pattern.vertices():
        index = key_index[key]
        pattern.vertex_attributes(key, 'xyz', xyz[index])


def compute_sag(pattern, opening):
    u, v = opening[0]
    if pattern.vertex_attribute(u, 'is_fixed'):
        a = pattern.vertex_attributes(u, 'xyz')
        aa = pattern.vertex_attributes(v, 'xyz')
    else:
        a = pattern.vertex_attributes(v, 'xyz')
        aa = pattern.vertex_attributes(u, 'xyz')
    u, v = opening[-1]
    if pattern.vertex_attribute(u, 'is_fixed'):
        b = pattern.vertex_attributes(u, 'xyz')
        bb = pattern.vertex_attributes(v, 'xyz')
    else:
        b = pattern.vertex_attributes(v, 'xyz')
        bb = pattern.vertex_attributes(u, 'xyz')
    span = distance_point_point_xy(a, b)
    apex = intersection_line_line_xy((a, aa), (b, bb))
    if apex is None:
        rise = 0.0
    else:
        midspan = midpoint_point_point_xy(a, b)
        rise = 0.5 * distance_point_point_xy(midspan, apex)
    sag = rise / span
    return sag


def _draw_labels(pattern, openings):
    labels = []
    for i, opening in enumerate(openings):
        points = pattern.datastructure.vertices_attributes('xyz', keys=opening)
        centroid = centroid_points(points)
        labels.append({'pos': centroid, 'text': str(i)})
    return compas_rhino.draw_labels(labels, layer=pattern.settings['layer'], clear=False, redraw=True)


# ==============================================================================
# Command
# ==============================================================================


TOL2 = 0.001 ** 2


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    relax = proxy.package("compas.numerical.fd_numpy")

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    # split the exterior boundary
    boundaries = pattern.datastructure.vertices_on_boundaries()
    exterior = boundaries[0]
    opening = []
    openings = [opening]
    for vertex in exterior:
        opening.append(vertex)
        if pattern.datastructure.vertex_attribute(vertex, 'is_anchor'):
            opening = [vertex]
            openings.append(opening)
    openings[-1] += openings[0]
    del openings[0]
    openings[:] = [opening for opening in openings if len(opening) > 2]

    draw_labels = partial(_draw_labels, pattern, openings)

    # draw a label per opening
    guids = draw_labels()

    # convert the list of vertices to a list of segments
    openings = [list(pairwise(opening)) for opening in openings]

    # compute current opening sags
    targets = []
    for opening in openings:
        sag = compute_sag(pattern.datastructure, opening)
        if sag < 0.05:
            sag = 0.05
        targets.append(sag)

    # compute current opening Qs
    Q = []
    for opening in openings:
        q = pattern.datastructure.edges_attribute('q', keys=opening)
        q = sum(q) / len(q)
        Q.append(q)
        pattern.datastructure.edges_attribute('q', q, keys=opening)

    # relax the pattern
    relax_pattern(pattern.datastructure, relax)

    # update Qs to match target sag
    while True:
        sags = [compute_sag(pattern.datastructure, opening) for opening in openings]
        if all((sag - target) ** 2 < TOL2 for sag, target in zip(sags, targets)):
            break
        for i in range(len(openings)):
            sag = sags[i]
            target = targets[i]
            q = Q[i]
            q = sag / target * q
            Q[i] = q
            opening = openings[i]
            pattern.datastructure.edges_attribute('q', Q[i], keys=opening)
        relax_pattern(pattern.datastructure, relax)

    compas_rhino.delete_objects(guids, purge=True)
    scene.update()
    guids = draw_labels()

    # allow user to select label
    # and specify a target sag
    options1 = ["Opening{}".format(i) for i, opening in enumerate(openings)] + ["ESC"]
    options2 = ["Sag5", "Sag10", "Sag15", "Sag20", "Sag25", "Sag30", "ESC"]

    while True:
        option1 = compas_rhino.rs.GetString("Select opening.", options1[-1], options1)
        if not option1 or option1 == "ESC":
            break
        N = int(option1[7:])

        while True:
            option2 = compas_rhino.rs.GetString("Select sag.", options2[-1], options2)
            if not option2 or option2 == "ESC":
                break
            targets[N] = float(option2[3:]) / 100

            while True:
                sags = [compute_sag(pattern.datastructure, opening) for opening in openings]
                if all((sag - target) ** 2 < TOL2 for sag, target in zip(sags, targets)):
                    break
                for i in range(len(openings)):
                    sag = sags[i]
                    target = targets[i]
                    q = Q[i]
                    q = sag / target * q
                    Q[i] = q
                    opening = openings[i]
                    pattern.datastructure.edges_attribute('q', Q[i], keys=opening)
                relax_pattern(pattern.datastructure, relax)

            compas_rhino.delete_objects(guids, purge=True)
            scene.update()
            guids = draw_labels()

    compas_rhino.delete_objects(guids, purge=True)
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
