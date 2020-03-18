from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import select_boundary_vertices
from compas_rv2.rhino import select_continuous_vertices


__commandname__ = "RV2form_select_vertices"


HERE = compas_rhino.get_document_dirname()


config = {
    "message": "FormDiagram Select Vertices",
    "options": [
        {"name": "Boundary", "action": select_boundary_vertices},
        {"name": "Continuous", "action": select_continuous_vertices}
    ]
}


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    rhinoform = scene.get("form")
    if not rhinoform:
        return

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    action["action"](rhinoform)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
