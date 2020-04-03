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
        return

    layer = pattern.settings['layer']
    group_vertices = "{}::vertices".format(layer)

    options = ['Continuous', 'Manual']
    option = compas_rhino.rs.GetString("Selection Type.", options[-1], options)

    if option == 'Continuous':
        compas_rhino.rs.ShowGroup(group_vertices)
        compas_rhino.rs.Redraw()
        temp = pattern.select_edges()
        keys = list(set(flatten([pattern.datastructure.continuous_vertices(key) for key in temp])))

    else:
        compas_rhino.rs.ShowGroup(group_vertices)
        compas_rhino.rs.Redraw()
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
