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

    u = scene.settings['pattern.from_surface.density.U']
    v = scene.settings['pattern.from_surface.density.V']

    options = ['U', 'V', 'ESC']
    while True:
        option = compas_rhino.rs.GetString("Density.", options[-1], options)
        if not option:
            break
        if option == 'ESC':
            break
        if option == 'U':
            u = compas_rhino.rs.GetInteger("Density U", u, 2, 100)
            continue
        if option == 'V':
            v = compas_rhino.rs.GetInteger("Density V", v, 2, 100)
            continue

    scene.settings['pattern.from_surface.density.U'] = u
    scene.settings['pattern.from_surface.density.V'] = v

    density = u, v
    pattern = RhinoSurface.from_guid(guid).uv_to_compas(cls=Pattern, density=density)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
