from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_move_vertices"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    layer = pattern.settings['pattern.layer']
    group_vertices = "{}::vertices".format(layer)

    compas_rhino.rs.ShowGroup(group_vertices)
    compas_rhino.rs.Redraw()

    keys = pattern.select_vertices()

    if keys:
        if pattern.move_vertices(keys):
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
