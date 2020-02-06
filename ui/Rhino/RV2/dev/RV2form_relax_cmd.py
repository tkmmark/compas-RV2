from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2form_relax"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    proxy = get_proxy()
    if not proxy:
        return

    proxy.package = "compas_tna.utilities"
    relax = proxy.relax_boundary_openings_proxy

    settings = RV2["settings"]
    rhinoform = RV2["scene"]["form"]

    if not rhinoform:
        return

    fixed = list(rhinoform.diagram.vertices_where({'is_fixed': True}))
    rhinoform.diagram.data = relax(rhinoform.diagram.data, fixed)

    rhinoform.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
