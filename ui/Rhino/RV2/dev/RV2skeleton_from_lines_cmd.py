from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.skeleton import Skeleton
from compas_rv2.rhino import RhinoSkeleton


__commandname__ = "RV2skeleton_from_lines"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    guids = compas_rhino.select_lines()
    if not guids:
        return

    lines = compas_rhino.get_line_coordinates(guids)
    skeleton = Skeleton.from_skeleton_lines(lines)
    if not skeleton:
        return

    compas_rhino.delete_objects(guids)

    rhinoskeleton = scene.add(skeleton, name='skeleton')
    rhinoskeleton.draw_skeleton_branches()
    rhinoskeleton.dynamic_draw_self()
    rhinoskeleton.draw_self()

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
