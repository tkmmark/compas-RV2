from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2pattern_relax"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    # replace this by simple FD
    # add version using DR for more control
    relax = proxy.package("compas_tna.utilities.relax_boundary_openings_proxy")

    rhinopattern = scene.get("pattern")

    if not rhinopattern:
        return

    fixed = list(rhinopattern.mesh.vertices_where({'is_fixed': True}))
    rhinopattern.mesh.data = relax(rhinopattern.mesh.data, fixed)

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
