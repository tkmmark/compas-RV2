from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rv2.rhino import get_scene

import RV2settings_objects_cmd
import RV2settings_solver_cmd


__commandname__ = "RV2toolbar_settings"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    options = ["ObjectSettings", "SolverSettings"]
    option = compas_rhino.rs.GetString("RV2 Settings", strings=options)

    if not option:
        return

    if option == "ObjectSettings":
        RV2settings_objects_cmd.RunCommand(True)

    elif option == "SolverSettings":
        RV2settings_solver_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
