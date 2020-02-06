from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2equilibrium_horizontal"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    proxy = get_proxy()
    if not proxy:
        return

    proxy.package = "compas_rv2.equilibrium"
    horizontal = proxy.horizontal_nodal_proxy

    settings = RV2["settings"]
    rhinoform = RV2["scene"]["form"]
    rhinoforce = RV2["scene"]["force"]

    if not rhinoform:
        return

    if not rhinoforce:
        return

    formdata, forcedata = horizontal(rhinoform.diagram.data, rhinoforce.diagram.data)

    rhinoform.diagram.data = formdata
    rhinoforce.diagram.data = forcedata

    rhinoform.draw(settings)
    rhinoforce.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
