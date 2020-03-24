from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2tna_horizontal"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    horizontal = proxy.package('compas_rv2.equilibrium.horizontal_nodal_proxy')

    form = scene.get('form')[0]
    force = scene.get('force')[0]

    if not form:
        return

    if not force:
        return

    formdata, forcedata = horizontal(form.datastructure.data, force.datastructure.data)

    form.datastructure.data = formdata
    force.datastructure.data = forcedata

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
