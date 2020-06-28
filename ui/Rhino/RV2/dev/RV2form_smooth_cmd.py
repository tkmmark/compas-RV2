from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.utilities import flatten


__commandname__ = "RV2form_smooth"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]

    anchors = list(form.datastructure.vertices_where({'is_anchor': True}))
    fixed = list(form.datastructure.vertices_where({'is_fixed': True}))
    fixed = list(set(anchors + fixed))

    options = ['True', 'False']
    option = compas_rhino.rs.GetString("Keep all boundaries fixed.", options[0], options)

    if not option:
        return

    if option == 'True':
        fixed = fixed + list(flatten(form.datastructure.vertices_on_boundaries()))

    form.datastructure.smooth_area(fixed=fixed)

    if thrust:
        thrust.settings['_is.valid'] = False

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
