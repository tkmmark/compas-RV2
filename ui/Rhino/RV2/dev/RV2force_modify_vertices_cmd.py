from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2force_modify_vertices"


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

    compas_rhino.rs.ShowGroup(group_vertices)
    compas_rhino.rs.Redraw()

    options = ["All", "Continuous", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)

    if not option:
        return

    elif option == "All":
        keys = list(force.datastructure.vertices())

    elif option == "Continuous":
        temp = force.select_edges()
        keys = list(set(flatten([force.datastructure.continuous_vertices(key) for key in temp])))

    elif option == "Manual":
        keys = force.select_vertices()

    public = [name for name in force.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
    if force.update_vertices_attributes(keys, names=public):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
