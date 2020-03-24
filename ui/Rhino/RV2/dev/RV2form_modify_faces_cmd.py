from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2form_modify_faces"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        return

    # is_loaded should be _is_loaded

    options = ['All', 'Parallel', 'ESC']
    option = compas_rhino.rs.GetString("Select Faces.", options[-1], options)

    if option == 'All':
        keys = list(form.datastructure.faces())

    elif option == 'Parallel':
        temp = form.select_edges()
        keys = list(set(flatten([form.datastructure.parallel_faces(key) for key in temp])))

    else:
        keys = form.select_faces()

    public = [name for name in form.datastructures.default_face_attributes.keys() if not name.startswith('_')]
    if form.update_faces_attributes(keys, names=public):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
