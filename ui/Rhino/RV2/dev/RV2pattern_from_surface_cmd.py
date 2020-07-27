from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoSurface
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import PatternObject
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import rv2_undo


__commandname__ = "RV2pattern_from_surface"


@rv2_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_surface()
    if not guid:
        return

    u = PatternObject.settings['from_surface.density.U']
    v = PatternObject.settings['from_surface.density.V']

    options = ['U', 'V']
    while True:
        option = compas_rhino.rs.GetString("Enter values for U and V:", strings=options)

        if not option:
            break

        if option == 'U':
            u = compas_rhino.rs.GetInteger("Density U", u, 2, 100)
            continue
        if option == 'V':
            v = compas_rhino.rs.GetInteger("Density V", v, 2, 100)
            continue

    density = u + 1, v + 1
    pattern = RhinoSurface.from_guid(guid).uv_to_compas(cls=Pattern, density=density)

    compas_rhino.rs.HideObject(guid)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    print("Pattern object successfully created. Input surface has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
