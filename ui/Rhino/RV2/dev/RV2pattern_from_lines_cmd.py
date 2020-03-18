from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.patterns import Pattern
from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_from_lines"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guids = compas_rhino.select_lines()
    if not guids:
        return

    pattern = Pattern.from_rhinolines(guids)

    # should the scene not be cleared at the start of this procedure?
    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
