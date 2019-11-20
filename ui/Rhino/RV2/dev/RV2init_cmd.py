from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

# replace this by from compas_cloud import Proxy
from compas.rpc import Proxy

__commandname__ = "RV2init"


def RunCommand(is_interactive):
    sc.sticky["RV2"] = {
        # the names of the settings can be split at the dot to allow for grouping
        "settings": {
            "layers.form": "RV2::FormDiagram",
            "layers.force": "RV2::ForceDiagram",
            "layers.thrust": "RV2::ThrustNetwork"},
            "file.dir": None,
            "file.name": None,
            "file.ext": 'rv2',
        "data": {
            "form": None,
            "force": None,
            "thrust": None}
        # solver settings?
    }
    p = Proxy()  # use a RV2-specific address (port)
    # display the "welcome" screen


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
