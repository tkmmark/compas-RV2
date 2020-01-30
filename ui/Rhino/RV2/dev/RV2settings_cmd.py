from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino
from compas_rhino.etoforms import TextForm


__commandname__ = "RV2settings"


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    rhinoform = sc.sticky["RV2"]["scene"]["form"]
    rhinoforce = sc.sticky["RV2"]["scene"]["force"]

    settings = sc.sticky["RV2"]["settings"]

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
