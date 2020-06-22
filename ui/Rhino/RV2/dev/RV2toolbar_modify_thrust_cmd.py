from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rv2.rhino import get_scene

import RV2thrust_attributes_cmd
import RV2thrust_move_supports_cmd


__commandname__ = "RV2toolbar_modify_thrust"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("thrust")[0]
    if not pattern:
        print("There is no ThrustDiagram in the scene.")
        return

    options = ["DiagramAttributes", "MoveSupports"]
    option = compas_rhino.rs.GetString("Modify form Diagram:", strings=options)

    if not option:
        return

    if option == "DiagramAttributes":
        RV2thrust_attributes_cmd.RunCommand(True)

    elif option == "MoveSupports":
        RV2thrust_move_supports_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
