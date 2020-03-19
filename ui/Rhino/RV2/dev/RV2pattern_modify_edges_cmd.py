from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_modify_edges"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]

    if not pattern:
        return

    option = compas_rhino.rs.GetString("Select Edges", "Boundary", ["Boundary", "Continuous", "Parallel"])

    if option == "Boundary":
        keys = list(pattern.mesh.edges_on_boundary())

    elif option == "Continuous":
        temp = pattern.select_edges()
        if temp:
            temp[:] = list(set(temp))
            keys = []
            for key in temp:
                keys += pattern.mesh.continuous_edges(key)

    elif option == "Parallel":
        temp = pattern.select_edges()
        if temp:
            temp[:] = list(set(temp))
            keys = []
            for key in temp:
                keys += pattern.mesh.parallel_edges(key)

    else:
        keys = None

    if pattern.update_edges_attributes(keys=keys):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
