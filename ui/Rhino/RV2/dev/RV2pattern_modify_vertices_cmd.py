from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2pattern_modify_vertices"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    layer = pattern.settings['layer']

    group_supports = "{}::vertices::supports".format(layer)
    group_fixed = "{}::vertices::fixed".format(layer)
    group_free = "{}::vertices::free".format(layer)

    options = ['Continuous', 'Manual']
    option = compas_rhino.rs.GetString("Selection Type.", options[-1], options)

    if option == 'Continuous':
        compas_rhino.rs.ShowGroup(group_supports)
        compas_rhino.rs.ShowGroup(group_fixed)
        compas_rhino.rs.HideGroup(group_free)
        compas_rhino.rs.Redraw()

        temp = pattern.select_edges()
        keys = list(set(flatten([pattern.datastructure.continuous_vertices(key) for key in temp])))

    else:
        compas_rhino.rs.ShowGroup(group_supports)
        compas_rhino.rs.ShowGroup(group_fixed)
        compas_rhino.rs.ShowGroup(group_free)
        compas_rhino.rs.Redraw()

        keys = pattern.select_vertices()

    # draw and highlight the selected vertices

    if keys:
        public = [name for name in pattern.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
        if pattern.update_vertices_attributes(keys, names=public):
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
