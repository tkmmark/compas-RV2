from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.datastructures import mesh_subdivide_quad


__commandname__ = "RV2pattern_subdivide"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    options = ["Finer", "Coarser"]
    while True:

        option = compas_rhino.rs.GetString("Select mode", strings=options)

        if not option:
            break

        if option == "Finer":
            subd = mesh_subdivide_quad(pattern.datastructure, k=1)
            for key, attr in pattern.datastructure.vertices(True):
                names = list(attr.keys())
                values = list(attr.values())
                subd.vertex_attributes(key, names, values)
            pattern.datastructure = subd
            scene.update()

        else:
            raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
