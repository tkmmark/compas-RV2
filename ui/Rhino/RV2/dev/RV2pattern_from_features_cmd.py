from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import get_scene
from compas_singular.datastructures.mesh.constraints import automated_smoothing_surface_constraints, automated_smoothing_constraints
from compas_singular.datastructures.mesh.relaxation import constrained_smoothing


__commandname__ = "RV2pattern_from_features"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    srf_guid = compas_rhino.select_surface("Select a surface.")
    if not srf_guid:
        return

    crv_guids = []
    pt_guids = compas_rhino.select_points("Optional. Select points for pole singularities.") or []

    box = compas_rhino.rs.BoundingBox([srf_guid])
    input_subdivision_spacing = 0.01 * compas_rhino.rs.Distance(box[0], box[6])

    mesh_edge_length = compas_rhino.rs.GetReal("Pattern edge-length target.", 1.0)

    # print("Decompose surface and generate a pattern...")
    pattern = Pattern.from_surface_and_features(input_subdivision_spacing, mesh_edge_length, srf_guid, crv_guids, pt_guids)
    # print("Pattern topology generated.")

    # print("Relax pattern on surface...")
    # kmax = compas_rhino.rs.GetInteger("Number of iterations for constrained Laplacian smoothing.", 50)
    # constraints = automated_smoothing_surface_constraints(pattern, srf_guid)
    # constraints.update(automated_smoothing_constraints(pattern, points=pt_guids, curves=crv_guids))
    # constrained_smoothing(pattern, kmax=kmax, damping=0.5, constraints=constraints, algorithm='area')
    # objs = set(constraints.values())
    # inputs = [srf_guid] + crv_guids + pt_guids
    # for obj in objs:
    #     if obj not in inputs:
    #         compas_rhino.rs.DeleteObject(obj)
    # for guid in inputs:
    #     compas_rhino.rs.HideObject(guid)
    # print("Pattern relaxed on surface.")

    compas_rhino.rs.HideObjects([srf_guid] + crv_guids + pt_guids)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    print('Pattern object successfully created. Input object has been hidden.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
