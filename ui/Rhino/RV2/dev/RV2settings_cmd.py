from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino


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
            form.draw(settings)
        if force:
            force.draw(settings)
        if thrust:
            thrust.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
