from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2equilibrium_vertical"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    vertical = proxy.package('compas_tna.equilibrium.vertical_from_zmax_proxy')

    rhinoform = scene.get('form')[0]
    rhinoforce = scene.get('force')[0]
    rhinothrust = scene.get('thrust')[0]

    if not rhinoform:
        return

    if not rhinoforce:
        return

    if not rhinothrust:
        return

    zmax = scene.settings['tna.vertical.zmax']

    formdata, scale = vertical(rhinoform.datastructure.data, zmax)

    rhinoforce.datastructure.attributes['scale'] = scale
    rhinoform.datastructure.data = formdata
    rhinothrust.datastructure.data = formdata
    rhinothrust.visible = True

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
