from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2equilibrium_vertical"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    proxy = get_proxy()
    if not proxy:
        return

    vertical = proxy.package("compas_tna.equilibrium.vertical_from_zmax_proxy")

    settings = RV2["settings"]
    rhinoform = RV2["scene"]["form"]
    rhinoforce = RV2["scene"]["force"]
    rhinothrust = RV2["scene"]["thrust"]
    zmax = settings["vertical.zmax"]

    if not rhinoform:
        return

    if not rhinoforce:
        return

    if not rhinothrust:
        return

    formdata, scale = vertical(rhinoform.diagram.data, zmax)

    rhinoforce.diagram.attributes['scale'] = scale

    rhinoform.diagram.data = formdata
    rhinothrust.diagram.data = formdata

    rhinoform.draw(settings)
    rhinothrust.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
