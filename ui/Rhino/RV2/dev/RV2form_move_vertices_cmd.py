from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2form_move_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        return

    layer = form.settings['layer']
    group_vertices = "{}::vertices".format(layer)

    options = ['Continuous', 'Manual']
    option = compas_rhino.rs.GetString("Selection Type.", options[-1], options)

    if option == 'Continuous':
        compas_rhino.rs.ShowGroup(group_vertices)
        compas_rhino.rs.Redraw()
        temp = form.select_edges()
        keys = list(set(flatten([form.datastructure.continuous_vertices(key) for key in temp])))

    else:
        compas_rhino.rs.ShowGroup(group_vertices)
        compas_rhino.rs.Redraw()
        keys = form.select_vertices()

    if keys:
        if form.move_vertices(keys):
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
