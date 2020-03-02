from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ThrustDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoThrustDiagram
from compas_rv2.rhino import select_filepath_open
from compas_rv2.rhino import get_rv2
from compas_rv2.rhino import get_scene


__commandname__ = "RV2form_from_obj"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    scene = get_scene()
    if not scene:
        return

    session = RV2["session"]
    root = session["cwd"] or HERE

    filepath = select_filepath_open(root, 'obj')
    if not filepath:
        return

    form = FormDiagram.from_obj(filepath)
    thrust = form.copy(cls=ThrustDiagram)

    scene.clear()
    scene.add(form, name='form')
    scene.add(thrust, name='thrust')
    scene.update()

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
