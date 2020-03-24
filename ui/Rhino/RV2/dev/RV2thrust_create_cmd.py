from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import ThrustDiagram
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram

__commandname__ = "RV2thrust_create"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    form = FormDiagram.from_mesh(pattern.datastructure)
    form.update_boundaries(feet=2)

    force = ForceDiagram.from_formdiagram(form)

    # this is not a good idea
    thrust = form.copy(cls=ThrustDiagram)

    scene.add(form, name='form')
    scene.add(force, name='force')
    scene.add(thrust, name='thrust')

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
