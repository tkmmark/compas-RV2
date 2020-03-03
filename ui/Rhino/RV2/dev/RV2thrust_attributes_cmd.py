from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import AttributeForm


__commandname__ = "RV2thrust_attributes"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    rhinothrustform = scene.get("thrust")

    if not rhinothrustform:
        return

    AttributeForm.from_diagram(rhinothrustform)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
