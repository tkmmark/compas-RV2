from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import select_vertices


__commandname__ = "RV2boundary_openings"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")

    if not pattern:
        return

    # how about any previously identified openings?
    # this only works if the outside space ahs already been broken up
    # using the anchors
    # and if the pattern has been relaxed

    # => this function might be redundant

    keys = pattern.select_faces()
    pattern.mesh.faces_attribute('is_unloaded', True, keys=keys)

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
