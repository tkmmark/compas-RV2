from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene



__commandname__ = "RV2pattern_move_vertices"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]

    if not pattern:
        return

    option = compas_rhino.rs.GetString("Select Vertices", "Boundary", ["Boundary", "Continuous"])

    if option == "Boundary":
        keys = list(pattern.datastructure.vertices_on_boundary(chained=False))

    elif option == "Continuous":
        temp = pattern.select_edges()
        if temp:
            temp[:] = list(set(temp))
            keys = []
            for key in temp:
                keys += pattern.datastructure.continuous_vertices(key)

    else:
        keys = None

    # this is not implemented yet in RV2.
    # add constrained movement => X, Y, Z

    if pattern.move_vertices(keys=keys):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
