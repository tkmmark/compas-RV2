from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy

from compas_singular.datastructures.mesh.constraints import automated_smoothing_surface_constraints, automated_smoothing_constraints
from compas_singular.datastructures.mesh.relaxation import constrained_smoothing


__commandname__ = "RV2pattern_from_features"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    srf_guid = compas_rhino.select_surface("Select a surface.")
    if not srf_guid:
        return

    crv_guids = []
    pt_guids = compas_rhino.select_points("Step 1/3 (Optional) - Select points for pole singularities.") or []

    box = compas_rhino.rs.BoundingBox([srf_guid])
    input_subdivision_spacing = 0.01 * compas_rhino.rs.Distance(box[0], box[6])

    mesh_edge_length = compas_rhino.rs.GetReal("Step 2/3 - Enter target length for edges.", 1.0)

    delaunay = proxy.function("compas.geometry.triangulation.triangulation_numpy.delaunay_from_points_numpy")

    pattern = Pattern.from_surface_and_features(input_subdivision_spacing, mesh_edge_length, srf_guid, crv_guids, pt_guids, delaunay)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    kmax = 10

    while True:
        option = compas_rhino.rs.GetString("Step 3/3 (Optional) - Press Enter to run constrained Laplacian smoothing or ESC to skip.", strings=['Iterations'])

        if option is None:
            break

        if not option:
            constraints = automated_smoothing_surface_constraints(pattern, srf_guid)
            constraints.update(automated_smoothing_constraints(pattern, points=pt_guids, curves=crv_guids))
            constrained_smoothing(pattern, kmax=kmax, damping=0.5, constraints=constraints, algorithm='area')
            objs = set(constraints.values())
            inputs = [srf_guid] + crv_guids + pt_guids
            for obj in objs:
                if obj not in inputs:
                    compas_rhino.rs.DeleteObject(obj)
            compas_rhino.rs.HideObjects(inputs)
            break

        if option == 'Iterations':
            new_kmax = compas_rhino.rs.GetInteger("Number of iterations:", kmax)
            if new_kmax or new_kmax is not None:
                kmax = new_kmax

    scene.update()

    print('Pattern object successfully created. Input object has been hidden.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
