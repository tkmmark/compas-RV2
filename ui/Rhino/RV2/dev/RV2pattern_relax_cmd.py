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

    # simple smoothing should be a separate command!

    relax = proxy.package("compas_tna.utilities.relax_boundary_openings_proxy")

    pattern = scene.get("pattern")[0]

    if not pattern:
        return

    fixed = list(pattern.datastructure.vertices_where({'is_fixed': True}))
    pattern.datastructure.data = relax(pattern.datastructure.data, fixed)

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
