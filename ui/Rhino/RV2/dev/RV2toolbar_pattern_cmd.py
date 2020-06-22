from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

import RV2pattern_from_lines_cmd
import RV2pattern_from_mesh_cmd
import RV2pattern_from_surface_cmd
import RV2pattern_from_skeleton_cmd
import RV2pattern_from_triangulation_cmd
import RV2pattern_from_features_cmd


__commandname__ = "RV2toolbar_pattern"


def RunCommand(is_interactive):

    options = ["FromLines", "FromMesh", "FromSurface", "FromSkeleton", "FromTriangulation", "FromFeatures"]
    option = compas_rhino.rs.GetString("Create Pattern:", strings=options)

    if not option:
        return

    elif option == "FromLines":
        RV2pattern_from_lines_cmd.RunCommand(True)

    elif option == "FromMesh":
        RV2pattern_from_mesh_cmd.RunCommand(True)

    elif option == "FromSurface":
        RV2pattern_from_surface_cmd.RunCommand(True)

    elif option == "FromSkeleton":
        RV2pattern_from_skeleton_cmd.RunCommand(True)

    elif option == "FromTriangulation":
        RV2pattern_from_triangulation_cmd.RunCommand(True)

    elif option == "FromFeatures":
        RV2pattern_from_features_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
