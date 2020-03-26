from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene
from compas_rv2.rhino import SettingsForm

__commandname__ = "RV2settings_solver"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    SettingsForm.from_settings(scene.settings, 'Solver')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
