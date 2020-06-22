from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2force_move_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    force = scene.get("force")[0]
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    layer = force.settings['layer']
    group_vertices = "{}::vertices".format(layer)

    options = ["Continuous", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)

    if not option:
        return

    if option == "Continuous":
        compas_rhino.rs.ShowGroup(group_vertices)
        compas_rhino.rs.Redraw()
        temp = force.select_edges()
        keys = list(set(flatten([force.datastructure.continuous_vertices(key) for key in temp])))

    elif option == "Manual":
        compas_rhino.rs.ShowGroup(group_vertices)
        compas_rhino.rs.Redraw()
        keys = force.select_vertices()

    if keys:
        if force.move_vertices(keys):
            force.datastructure.update_angle_deviations()
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
