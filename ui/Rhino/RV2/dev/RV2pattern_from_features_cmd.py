from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key
from compas.utilities import linspace

import compas_rhino
from compas_rhino.artists import MeshArtist
from compas_rhino.geometry import RhinoPoint

from compas_singular.rhino import automated_smoothing_surface_constraints
from compas_singular.rhino import automated_smoothing_constraints
from compas_singular.rhino import constrained_smoothing
from compas_singular.rhino import RhinoSurface
from compas_singular.rhino import RhinoCurve

from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas_rv2.rhino import rv2_undo


__commandname__ = "RV2pattern_from_features"


@rv2_undo
def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    # Get input data.
    surf_guid = compas_rhino.select_surface("Select a surface to decompose.")
    if not surf_guid:
        return
    point_guids = compas_rhino.select_points("Select points to include in the decomposition.")
    curve_guids = []

    surface = RhinoSurface.from_guid(surf_guid)
    curves = [RhinoCurve.from_guid(guid) for guid in curve_guids]
    points = [RhinoPoint.from_guid(guid) for guid in point_guids]

    # Compute the feature discretisation length.
    box = compas_rhino.rs.BoundingBox([surf_guid])
    diagonal = compas_rhino.rs.Distance(box[0], box[6])
    D = 0.01 * diagonal

    # Get the target length for the final quad mesh.
    L = compas_rhino.rs.GetReal("Define the target edge length of the pattern.", 1.0)

    # Generate the pattern
    pattern = Pattern.from_surface_and_features(D, L, surf_guid, curve_guids, point_guids)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    # Constrain mesh components to the feature geometry.
    constraints = automated_smoothing_surface_constraints(pattern, surface)
    constraints.update(
        automated_smoothing_constraints(pattern, rhinopoints=points, rhinocurves=curves)
    )

    # Smooth with constraints.
    constrained_smoothing(
        pattern, kmax=10, damping=0.5, constraints=constraints, algorithm="area"
    )

    scene.update()

    print('Pattern object successfully created. Input object has been hidden.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
