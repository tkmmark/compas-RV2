from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoSurface
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import PatternObject
from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_from_features"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    srf_guid = compas_rhino.select_surface("Select a surface.")
    if not srf_guid:
        return

    crv_guids = compas_rhino.select_curves("Optional. Select curves to align the pattern.") or []
    pt_guids = compas_rhino.select_points("Optional. Select points for pole singularities.") or []

    input_subdivision_spacing = compas_rhino.rs.GetReal("Input subdivision spacing", 1.0)
    box = compas_rhino.rs.BoundingBox([srf_guid])
    input_subdivision_spacing = 0.05 * compas_rhino.rs.Distance(box[0], box[6])

    mesh_edge_length = compas_rhino.rs.GetReal("Pattern edge-length target.", 1.0)

    pattern = Pattern.from_surface_and_features(input_subdivision_spacing, mesh_edge_length, srf_guid, crv_guids, pt_guids)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    print('Pattern object successfully created.')

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
