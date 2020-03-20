from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene


__commandname__ = "RV2form_modify_faces"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")

    if not pattern:
        return

    option = compas_rhino.rs.GetString("Select Faces", "Boundary", ["Boundary", "Parallel"])

    if option == "Boundary":
        keys = list(pattern.datastructure.faces_on_boundary())

    elif option == "Parallel":
        temp = pattern.select_edges()
        if temp:
            temp[:] = list(set(temp))
            keys = []
            for key in temp:
                keys += pattern.datastructure.parallel_faces(key)

    else:
        keys = None

    if pattern.update_faces_attributes(keys=keys):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
