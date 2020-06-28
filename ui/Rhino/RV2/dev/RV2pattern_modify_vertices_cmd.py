from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2pattern_modify_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    options = ["AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual"]

    while True:
        option = compas_rhino.rs.GetString("Selection mode:", strings=options)
        if not option:
            return

        if option == "Corners":
            keys = []
            for key in pattern.datastructure.vertices_on_boundary():
                if pattern.datastructure.vertex_degree(key) == 2:
                    keys.append(key)

        elif option == "AllBoundaryVertices":
            keys = pattern.datastructure.vertices_on_boundary()

        elif option == "ByContinuousEdges":
            temp = pattern.select_edges()
            keys = list(set(flatten([pattern.datastructure.vertices_on_edge_loop(key) for key in temp])))

        elif option == "Manual":
            keys = pattern.select_vertices()

        if keys:
            public = [name for name in pattern.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
            if pattern.update_vertices_attributes(keys, names=public):
                scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
