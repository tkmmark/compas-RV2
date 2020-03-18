from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.skeleton import Skeleton


__commandname__ = "RV2skeleton_from_point"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    guids = compas_rhino.select_point()
    if not guids:
        return

    pt = compas_rhino.get_point_coordinates([guids])[0]
    skeleton = Skeleton.from_center_point(pt)
    if not skeleton:
        return

    compas_rhino.delete_objects([guids])

    rhinoskeleton = scene.add(skeleton, 'skeleton')
    rhinoskeleton.dynamic_draw_self()
    rhinoskeleton.draw_self()


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
