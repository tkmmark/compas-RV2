from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene


__commandname__ = "RV2analysis_show_colors"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        return

    force = scene.get("force")[0]
    if not force:
        return

    thrust = scene.get("thrust")[0]
    if not thrust:
        return

    if not form.settings['show.color.analysis']:
        form.settings['show.color.analysis'] = True
        force.settings['show.color.analysis'] = True
        thrust.settings['show.color.analysis'] = True
        print('Color analysis mode ON.')

    else:
        form.settings['show.color.analysis'] = False
        force.settings['show.color.analysis'] = False
        thrust.settings['show.color.analysis'] = False
        print('Color analysis mode OFF.')

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
