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

    # mark all fixed vertices as anchors
    # mark all leaves as anchors

    options = ["Select", "Unselect"]
    option1 = compas_rhino.rs.GetString("Select or unselect vertices as supports:", strings=options)

    if not option1:
        return

    layer = pattern.settings['layer']
    group_supports = "{}::vertices::supports".format(layer)

    compas_rhino.rs.ShowGroup(group_supports)
    compas_rhino.rs.Redraw()

    options = ["InheritFromPattern", "AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual"]

    while True:
        option2 = compas_rhino.rs.GetString("Selection mode:", strings=options)

        if not option2:
            return

        elif option2 == "Corners":
            keys = []
            for key in pattern.datastructure.vertices_on_boundary():
                if pattern.datastructure.vertex_degree(key) == 2:
                    keys.append(key)

        elif option2 == "InheritFromPattern":
            keys = pattern.datastructure.vertices_where({'is_fixed': True})

        elif option2 == "AllBoundaryVertices":
            keys = pattern.datastructure.vertices_on_boundary()



        elif option2 == 'ByContinuousEdges':
            temp = pattern.select_edges()
            keys = list(set(flatten([pattern.datastructure.continuous_vertices(key) for key in temp])))

        elif option2 == 'Manual':
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
