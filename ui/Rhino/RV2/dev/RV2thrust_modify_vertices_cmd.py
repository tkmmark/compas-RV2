from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2thrust_modify_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    # hide the form vertices
    form_vertices = "{}::vertices".format(form.settings['layer'])
    compas_rhino.rs.HideGroup(form_vertices)

    # show the thrust vertices
    thrust_vertices = "{}::vertices".format(thrust.settings['layer'])
    compas_rhino.rs.ShowGroup(thrust_vertices)

    compas_rhino.rs.Redraw()

    # selection options
    options = ["Continuous", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "Continuous":
        temp = thrust.select_edges()
        keys = list(set(flatten([thrust.datastructure.vertices_on_edge_loop(key) for key in temp])))

    elif option == "Manual":
        keys = thrust.select_vertices()

    public = [name for name in thrust.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
    thrust.update_vertices_attributes(keys, names=public)

    # the scene needs to be updated
    # even if the vertices where not modified
    # to reset group visibility to the configuration of settings
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
