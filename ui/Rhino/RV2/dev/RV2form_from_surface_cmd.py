from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ThrustDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoThrustDiagram
from compas_rv2.rhino import get_scene

__commandname__ = "RV2form_from_surface"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_surface()
    if not guid:
        return

    form = FormDiagram.from_rhinosurface(guid)
    thrust = form.copy(cls=ThrustDiagram)

    scene.clear()
    scene.add(form, key='form')
    scene.add(thrust, key='thrust')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
