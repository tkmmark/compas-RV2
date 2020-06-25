from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene


__commandname__ = "RV2thrust_move_supports"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    thrust = scene.get("thrust")[0]
    form = scene.get("form")[0]

    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    layer = thrust.settings['layer']
    group_vertices = "{}::vertices".format(layer)

    compas_rhino.rs.ShowGroup(group_vertices)
    compas_rhino.rs.Redraw()
    keys = thrust.select_vertices()
    keys[:] = [key for key in keys if thrust.datastructure.vertex_attribute(key, 'is_anchor')]

    if keys:
        if thrust.move_vertices_vertical(keys):
            for key in keys:
                z = thrust.datastructure.vertex_attribute(key, 'z')
                form.datastructure.vertex_attribute(key, 'z', z)
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
