from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino

from compas_rv2.rhino import RhinoDiagram


__commandname__ = "RV2settings"


def RunCommand(is_interactive):
    # can this be moved to a decorator
    if "RV2" not in sc.sticky:
        raise Exception("Initialise the plugin first!")

    form = sc.sticky["RV2"]["data"]["form"]
    force = sc.sticky["RV2"]["data"]["force"]
    thrust = sc.sticky["RV2"]["data"]["thrust"]

    settings = sc.sticky["RV2"]["settings"]

    if compas_rhino.update_settings(settings):
        if form:
            rhinoform = RhinoDiagram(form)
            rhinoform.draw(settings)
        if force:
            rhinoforce = RhinoDiagram(force)
            rhinoforce.draw(settings)
        if thrust:
            rhinothrust = RhinoDiagram(thrust)
            rhinothrust.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
