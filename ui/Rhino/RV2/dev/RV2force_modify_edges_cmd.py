from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten

__commandname__ = "RV2force_modify_edges"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    force = scene.get("force")[0]
    if not force:
        return

    keys = force.select_edges()

    # is this necessary with the special update dialogs?
    public = [name for name in force.datastructure.default_edge_attributes.keys() if not name.startswith('_')]
    if force.update_edges_attributes(keys, names=public):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
