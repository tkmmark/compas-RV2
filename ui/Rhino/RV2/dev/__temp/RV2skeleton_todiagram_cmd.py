from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.datastructures import ThrustDiagram
from compas_rv2.rhino import get_scene

__commandname__ = "RV2skeleton_todiagram"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    rhinoskeleton = scene.get('skeleton')[0]

    if not rhinoskeleton:
        return

    form = rhinoskeleton.diagram.to_form()
    if not form:
        return
    thrust = form.copy(cls=ThrustDiagram)

    scene.clear()
    scene.add(form, name='form')
    scene.add(thrust, name='thrust', visible=False)
    scene.update()

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
