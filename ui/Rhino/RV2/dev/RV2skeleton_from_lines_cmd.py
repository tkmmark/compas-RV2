from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2
from compas_rv2.skeleton import Skeleton
from compas_rv2.rhino import RhinoSkeleton


__commandname__ = "RV2skeleton_from_lines"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    scene = RV2["scene"]

    guids = compas_rhino.select_lines()
    if not guids:
        return

    lines = compas_rhino.get_line_coordinates(guids)
    skeleton = Skeleton.from_skeleton_lines(lines)
    if not skeleton:
        return

    compas_rhino.delete_objects(guids)

    rhinoskeleton = RhinoSkeleton(skeleton)
    rhinoskeleton.draw_skeleton_branches()
    rhinoskeleton.dynamic_draw_self()
    rhinoskeleton.draw_self()

    scene["skeleton"] = rhinoskeleton


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
