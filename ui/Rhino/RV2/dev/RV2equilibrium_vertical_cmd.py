from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rv2.rhino import RhinoFormDiagram


__commandname__ = "RV2equilibrium_vertical"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    settings = RV2["settings"]
    form = RV2["data"]["form"]
    force = RV2["data"]["force"]

    proxy = sc.sticky["RV2.proxy"]

    if not form:
        return

    if not force:
        return

    if not proxy:
        return

    proxy.package = "compas_rv2.equilibrium"
    vertical = proxy.vertical_nodal_proxy

    form.data = vertical(form.data)

    formdiagram = RhinoFormDiagram(form)
    formdiagram.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
