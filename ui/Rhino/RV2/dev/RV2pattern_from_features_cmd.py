from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key
from compas.utilities import linspace

import compas_rhino
from compas_rhino.artists import MeshArtist
from compas_rhino.geometry import RhinoPoint

from compas_singular.algorithms import SkeletonDecomposition
from compas_singular.algorithms import boundary_triangulation
from compas_singular.rhino import RhinoSurface
from compas_singular.rhino import RhinoCurve
from compas_singular.rhino import automated_smoothing_surface_constraints
from compas_singular.rhino import automated_smoothing_constraints
from compas_singular.rhino import constrained_smoothing

from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas_rv2.rhino import rv2_undo


__commandname__ = "RV2pattern_from_features"


def pattern_from_features(srf_guid, crv_quids, pt_guids, L):
    # Wrap the inputs.
    surface = RhinoSurface.from_guid(srf_guid)
    curves = [RhinoCurve.from_guid(guid) for guid in crv_guids]
    points = [RhinoPoint.from_guid(guid) for guid in pt_guids]

    # Compute the feature discretisation length.
    box = compas_rhino.rs.BoundingBox([srf_guid])
    diagonal = compas_rhino.rs.Distance(box[0], box[6])
    D = 0.01 * diagonal

    # Process the input surface.
    result = surface.discrete_mapping(D, crv_guids=crv_guids, pt_guids=pt_guids)
    outer_boundary, inner_boundaries, polyline_features, point_features = result

    # Triangulate the input surface.
    trimesh = boundary_triangulation(*result, delaunay=delaunay)

    # Make a decomposition mesh from the triangulation.
    decomposition = SkeletonDecomposition.from_mesh(trimesh)

    # Generate a coarse mesh from the decomposition.
    coarsemesh = decomposition.decomposition_mesh(point_features)

    # Map coarse mesh edges to surface curve discretisations.
    gkey_vertex = {geometric_key(coarsemesh.vertex_coordinates(vertex)): vertex for vertex in coarsemesh.vertices()}
    edge_curve = {}
    for polyline in decomposition.polylines:
        curve = compas_rhino.rs.AddInterpCrvOnSrfUV(srf_guid, [point[:2] for point in polyline])
        u = gkey_vertex[geometric_key(polyline[0])]
        v = gkey_vertex[geometric_key(polyline[-1])]
        edge_curve[u, v] = [
            compas_rhino.rs.EvaluateCurve(curve, compas_rhino.rs.CurveParameter(curve, t))
            for t in linspace(0, 1, 100)]
        compas_rhino.delete_object(curve)

    # Densify the coarse mesh.
    coarsemesh.collect_strips()
    coarsemesh.set_strips_density_target(L)
    coarsemesh.densification(edges_to_curves=edge_curve)
    densemesh = coarsemesh.get_quad_mesh()

    # Create pattern.
    pattern = Pattern.from_vertices_and_faces(*densemesh.to_vertices_and_faces())

    # Constrain mesh components to the feature geometry.
    constraints = automated_smoothing_surface_constraints(pattern, surface)
    constraints.update(
        automated_smoothing_constraints(pattern, rhinopoints=points, rhinocurves=curves))

    # Smooth with constraints.
    constrained_smoothing(
        pattern, kmax=10, damping=0.5, constraints=constraints, algorithm="area")

    return pattern


@rv2_undo
def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    # Get input data.
    srf_guid = compas_rhino.select_surface("Select a surface to decompose.")
    if not srf_guid:
        return

    crv_guids = []
    # crv_guids = compas_rhino.select_curves("Select curves to include in the decomposition.")
    pt_guids = compas_rhino.select_points("Select points to include in the decomposition.")

    # Get the target length for the final quad mesh.
    L = compas_rhino.rs.GetReal("Define the target edge length of the pattern.", 1.0)

    # Generate the pattern
    pattern = pattern_from_features(srf_guid, crv_guids, pt_guids, L)
    if not pattern:
        return

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    print('Pattern object successfully created. Input object has been hidden.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
