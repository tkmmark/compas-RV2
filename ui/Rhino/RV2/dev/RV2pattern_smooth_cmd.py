from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.datastructures import mesh_smooth_area


__commandname__ = "RV2pattern_smooth"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    fixed = list(pattern.datastructure.vertices_where({'is_fixed': True}))
    mesh_smooth_area(pattern.datastructure, fixed=fixed)

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
