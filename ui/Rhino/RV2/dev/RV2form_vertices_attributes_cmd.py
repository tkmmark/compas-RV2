from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino

from compas_rv2.rhino import RhinoDiagram


__commandname__ = "RV2form_vertices_attributes"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        raise Exception("Initialise the plugin first!")

    RV2 = sc.sticky["RV2"]
    form = RV2["data"]["form"]

    if not form:
        return

    diagram = RhinoDiagram(form)

    if diagram.update_vertices_attributes():
        diagram.draw(RV2["settings"])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
