from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoSurface
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import get_scene


__commandname__ = "RV2pattern_from_surface"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_surface()
    if not guid:
        return

    density = 10, 10
    pattern = RhinoSurface.from_guid(guid).uv_to_compas(cls=Pattern, density=density)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
