from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino


__commandname__ = "RV2_settings"


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        raise Exception("Initialise the plugin first!")

    settings = sc.sticky["RV2"]

    if compas_rhino.update_settings(settings):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
