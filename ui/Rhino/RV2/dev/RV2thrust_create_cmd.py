from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import ThrustDiagram

__commandname__ = "RV2thrust_create"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    thrust = ThrustDiagram.from_pattern(pattern.datastructure)

    scene.add(thrust, name='thrust')
    scene.add(thrust.form, name='form')
    scene.add(thrust.force, name='force')

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
