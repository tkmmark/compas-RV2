from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene


__commandname__ = "RV2analysis_show_pipes"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    thrust = scene.get("thrust")[0]
    if not thrust:
        return

    if not thrust.settings['show.pipes']:
        thrust.settings['show.pipes'] = True

    else:
        thrust.settings['show.pipes'] = False

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
