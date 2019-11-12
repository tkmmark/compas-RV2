from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc


__commandname__ = "RV2_init"


def RunCommand(is_interactive):
    sc.sticky["RV2"] = {
        "settings": {
            "layers.form": "RV2::FormDiagram",
            "layers.force": "RV2::ForceDiagram",
            "layers.thrust": "RV2::ThrustNetwork",
        },
        "form": None,
        "force": None,
        "thrust": None
    }


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
