from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2equilibrium_horizontal"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    proxy.package = "compas_rv2.equilibrium"
    horizontal = proxy.horizontal_nodal_proxy

    rhinoform = scene.get("form")
    rhinoforce = scene.get("force")

    if not rhinoform:
        return

    if not rhinoforce:
        return

    formdata, forcedata = horizontal(rhinoform.diagram.data, rhinoforce.diagram.data)

    rhinoform.diagram.data = formdata
    rhinoforce.diagram.data = forcedata

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
