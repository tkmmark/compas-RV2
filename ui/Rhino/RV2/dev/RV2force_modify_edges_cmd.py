from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2force_modify_edges"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    force = scene.get("force")[0]
    if not force:
        return

    options = ["Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)

    if not option:
        return

    elif option == "Continuous":
        temp = force.select_edges()
        keys = list(set(flatten([force.datastructure.continuous_edges(key) for key in temp])))

    elif option == "Parallel":
        temp = force.select_edges()
        keys = list(set(flatten([force.datastructure.parallel_edges(key) for key in temp])))

    elif option == "Manual":
        keys = force.select_edges()

    if keys:
        public = [name for name in force.datastructure.default_edge_attributes.keys() if not name.startswith("_")]
        if force.update_edges_attributes(keys, names=public):
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
