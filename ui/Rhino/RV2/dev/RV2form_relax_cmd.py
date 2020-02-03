from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm


__commandname__ = "RV2form_relax"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    settings = RV2["settings"]
    rhinoform = RV2["scene"]["form"]

    proxy = sc.sticky["RV2.proxy"]

    if not rhinoform:
        return

    if not proxy:
        return

    proxy.package = "compas_tna.utilities"
    relax = proxy.relax_boundary_openings_proxy

    fixed = list(rhinoform.diagram.vertices_where({'is_fixed': True}))
    rhinoform.diagram.data = relax(rhinoform.diagram.data, fixed)

    rhinoform.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
