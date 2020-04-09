from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import ThrustDiagram
from compas_rv2.datastructures import FormDiagram
from compas.geometry import subtract_vectors
from compas.geometry import length_vector


__commandname__ = "RV2form"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    form = FormDiagram.from_pattern(pattern.datastructure)
    form.edges_attribute('fmin', 0.5)
    form.vertices_attribute('_is_fixed', False)

    thrust = form.copy(cls=ThrustDiagram)

    bbox_form = form.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox_form[2], bbox_form[0]))
    zmax = 0.25 * diagonal

    scene.settings['tna.vertical.zmax'] = round(zmax, 1)
    scene.clear()
    scene.add(form, name='form')
    scene.add(thrust, name='thrust')
    scene.update()

    print('FormDiagram object successfully created.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
