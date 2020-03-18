from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoMesh
from compas_rv2.patterns import Pattern
from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_from_mesh"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    pattern = RhinoMesh.from_guid(guid).to_compas(cls=Pattern)

    # should the scene not be cleared at the start of this procedure?
    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
