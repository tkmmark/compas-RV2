from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rv2.rhino import get_scene

import RV2pattern_relax_cmd
import RV2pattern_smooth_cmd
import RV2pattern_modify_vertices_cmd
import RV2pattern_modify_edges_cmd
import RV2pattern_move_vertices_cmd
import RV2pattern_delete_cmd


__commandname__ = "RV2toolbar_modify_pattern"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("force")[0]
    if not pattern:
        print("There is no ForceDiagram in the scene.")
        return

    options = ["Relax", "Smooth", "ModifyVertices", "ModifyEdges", "MoveVertices", "DeleteVertices"]
    option = compas_rhino.rs.GetString("Modify pattern:", strings=options)

    if not option:
        return

    if option == "Relax":
        RV2pattern_relax_cmd.RunCommand(True)

    elif option == "Smooth":
        RV2pattern_smooth_cmd.RunCommand(True)

    elif option == "ModifyVertices":
        RV2pattern_modify_vertices_cmd.RunCommand(True)

    elif option == "ModifyEdges":
        RV2pattern_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV2pattern_move_vertices_cmd.RunCommand(True)

    elif option == "DeleteVertices":
        RV2pattern_delete_cmd.RunCommand(True)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
