from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten


__commandname__ = "RV2pattern_modify_faces"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")
    if not pattern:
        return

    options = ['Manual', 'All', 'Openings', 'Holes', 'Parallel']
    option = compas_rhino.rs.GetString("Select Faces.", options[0], options)

    if option == 'All':
        keys = list(pattern.datastructure.faces())

    elif option == 'Openings':
        # select the faces around an opening
        # draw dots in openings
        # allow user to select dots
        raise NotImplementedError

    elif option == 'Holes':
        # select the faces around a hole
        # draw dots in holes
        # allow user to select dots
        raise NotImplementedError

    elif option == 'Parallel':
        temp = pattern.select_edges()
        keys = list(set(flatten([pattern.datastructure.parallel_faces(key) for key in temp])))

    else:
        keys = pattern.select_faces()

    public = [name for name in pattern.datastructures.default_face_attributes.keys() if not name.startswith('_')]
    if pattern.update_faces_attributes(keys, names=public):
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
