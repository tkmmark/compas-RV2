from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene


__commandname__ = "RV2analysis_show_colors"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    if scene.settings['rv2']['visualization.mode.force']:
        print('Visualization Mode: Force is ON.')
        scene.settings['rv2']['visualization.mode.force'] = False
    else:
        scene.settings['rv2']['visualization.mode.force'] = True
        print('Visualization Mode: Force is OFF.')

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
