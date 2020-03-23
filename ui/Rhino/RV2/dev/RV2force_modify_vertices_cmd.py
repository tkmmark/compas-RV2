from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene


__commandname__ = "RV2force_modify_vertices"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    force = scene.get("force")[0]
    if not force:
        return

    keys = force.select_vertices()

    public = [name for name in force.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
    if force.update_vertices_attributes(keys, names=public):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
