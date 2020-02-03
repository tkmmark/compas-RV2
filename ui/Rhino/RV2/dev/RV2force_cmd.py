from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rv2.datastructures import ForceDiagram
from compas_rv2.rhino import RhinoForceDiagram
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import Translation


__commandname__ = "RV2force"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    settings = RV2["settings"]
    rhinoform = RV2["scene"]["form"]

    if not rhinoform:
        return

    force = ForceDiagram.from_formdiagram(rhinoform.diagram)
    bbox = force.bounding_box()

    a = bbox[0]
    b = bbox[1]

    ab = subtract_vectors(b, a)
    ab = scale_vector(ab, 1.5)

    T = Translation(ab)

    force.transform(T)

    rhinoforce = RhinoForceDiagram(force)
    rhinoforce.draw(settings)

    RV2["scene"]["force"] = rhinoforce


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
