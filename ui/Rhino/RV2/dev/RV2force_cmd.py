from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rv2.diagrams import ForceDiagram
from compas_rv2.rhino import RhinoForceDiagram


__commandname__ = "RV2force"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    settings = RV2["settings"]
    form = RV2["data"]["form"]

    if not form:
        return

    force = ForceDiagram.from_formdiagram(form)

    forcediagram = RhinoForceDiagram(force)
    forcediagram.draw(settings)

    RV2["data"]["force"] = force


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
