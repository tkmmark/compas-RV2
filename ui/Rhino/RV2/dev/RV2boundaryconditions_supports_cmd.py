from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten

__commandname__ = "RV2boundaryconditions_supports"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    options = ["Select", "Unselect", "ESC"]
    option1 = compas_rhino.rs.GetString("Supports", options[-1], options)
    if not option1 or option1 == 'ESC':
        return

    layer = pattern.settings['layer']
    group_supports = "{}::vertices::supports".format(layer)

    compas_rhino.rs.ShowGroup(group_supports)
    compas_rhino.rs.Redraw()

    options = ["Continuous", "Manual", "ESC"]
    while True:
        option2 = compas_rhino.rs.GetString("Selection Mode.", options[-1], options)
        if not option2 or option2 == 'ESC':
            return

        if option2 == 'Continuous':
            temp = pattern.select_edges()
            keys = list(set(flatten([pattern.datastructure.continuous_vertices(key) for key in temp])))

        else:
            keys = pattern.select_vertices()

        if keys:
            value = option1 == "Select"
            pattern.datastructure.vertices_attribute('is_anchor', value, keys=keys)

        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
