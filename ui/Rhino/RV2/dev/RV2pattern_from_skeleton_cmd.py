from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.patterns import Pattern


__commandname__ = "RV2pattern_from_skeleton"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    # should the scene be cleared at the start of this procedure?

    # skeleton from lines
    # pattern from skeleton / skeleton to pattern


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
