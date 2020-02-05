from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2


__commandname__ = "RV2settings"


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    rhinoform = RV2["scene"]["form"]
    rhinoforce = RV2["scene"]["force"]

    settings = RV2["settings"]

    if compas_rhino.update_settings(settings):
        if rhinoform:
            rhinoform.draw(settings)
        if rhinoforce:
            rhinoforce.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
