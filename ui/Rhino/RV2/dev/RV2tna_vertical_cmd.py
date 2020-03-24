from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2tna_vertical"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    vertical = proxy.package('compas_tna.equilibrium.vertical_from_zmax_proxy')

    form = scene.get('form')[0]
    force = scene.get('force')[0]
    thrust = scene.get('thrust')[0]

    if not form:
        return

    if not force:
        return

    if not thrust:
        return

    zmax = scene.settings['tna.vertical.zmax']
    kmax = scene.settings['tna.vertical.kmax']

    formdata, scale = vertical(form.datastructure.data, zmax, kmax=kmax)

    force.datastructure.attributes['scale'] = scale
    form.datastructure.data = formdata
    thrust.datastructure.data = formdata
    thrust.visible = True

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
