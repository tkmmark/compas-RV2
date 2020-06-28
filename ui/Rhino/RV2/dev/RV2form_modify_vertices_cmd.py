from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2form_modify_vertices"


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

    # hide the thrust vertices
    thrust_vertices = "{}::vertices".format(thrust.settings['layer'])
    compas_rhino.rs.HideGroup(thrust_vertices)

    # show the form vertices
    form_vertices = "{}::vertices".format(form.settings['layer'])
    compas_rhino.rs.ShowGroup(form_vertices)

    compas_rhino.rs.Redraw()

    # selection options
    options = ["All", "Continuous", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "All":
        keys = list(form.datastructure.vertices())

    elif option == "Continuous":
        temp = form.select_edges()
        keys = list(set(flatten([form.datastructure.vertices_on_edge_loop(key) for key in temp])))

    elif option == "Manual":
        keys = form.select_vertices()

    public = [name for name in form.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
    form.update_vertices_attributes(keys, names=public)

    # the scene needs to be updated
    # even if the vertices where not modified
    # to reset group visibility to the configuration of settings
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
