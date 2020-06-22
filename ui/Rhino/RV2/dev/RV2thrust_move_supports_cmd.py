from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene


__commandname__ = "RV2thrust_move_supports"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    thrust = scene.get("thrust")[0]

    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
