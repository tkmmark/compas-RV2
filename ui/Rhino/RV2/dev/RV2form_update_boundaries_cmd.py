from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm


__commandname__ = "RV2form_update_boundaries"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    settings = RV2["settings"]
    rhinoform = RV2["scene"]["form"]

    if not rhinoform:
        return

    rhinoform.diagram.update_boundaries(feet=2)
    rhinoform.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
