from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ThrustDiagram

__commandname__ = "RV2form_create"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")

    if not pattern:
        # notify the user
        return

    form = FormDiagram.from_pattern(pattern.mesh)
    thrust = FormDiagram.copy(cls=ThrustDiagram)

    scene.add(form, name='form')
    scene.add(thrust, name='thrust')

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)