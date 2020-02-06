from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2


__commandname__ = "RV2force_update_faces"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    settings = RV2["settings"]
    rhinoforce = RV2["scene"]["force"]

    if not rhinoforce:
        return

    if rhinoforce.update_faces_attributes():
        rhinoforce.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
