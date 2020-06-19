from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_from_features"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
