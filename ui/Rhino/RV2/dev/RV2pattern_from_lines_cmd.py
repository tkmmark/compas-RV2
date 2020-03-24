from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.datastructures import Pattern
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

    lines = compas_rhino.get_line_coordinates(guids)
    pattern = Pattern.from_lines(lines, delete_boundary_face=True)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
