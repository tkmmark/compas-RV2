from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2form_relax"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    relax = proxy.package("compas_tna.utilities.relax_boundary_openings_proxy")

    rhinoform = scene.get("form")[0]

    if not rhinoform:
        return

    fixed = list(rhinoform.diagram.vertices_where({'is_fixed': True}))
    rhinoform.diagram.data = relax(rhinoform.diagram.data, fixed)

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
