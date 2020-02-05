from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rv2.rhino import get_rv2
from compas_rv2.rhino import PropertySheet


__commandname__ = "RV2form_attributes"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    RV2 = sc.sticky["RV2"]
    rhinoform = RV2["scene"]["form"]

    if not rhinoform:
        return

    PropertySheet.from_diagram(rhinoform)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
