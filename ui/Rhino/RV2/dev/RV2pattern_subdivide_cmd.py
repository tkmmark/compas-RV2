from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.datastructures import mesh_subdivide_quad


__commandname__ = "RV2pattern_subdivide"


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

    # options = ['Finer', 'Coarser', 'ESC']
    # while True:
    #     option = compas_rhino.rs.GetString('Select mode', options[-1], options)
    #     if not option or option == 'ESC':
    #         break

    #     if option == 'Finer':
    #         mesh_subdivide_quad(pattern.datastructure, k=1)

    # scene.update()

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
