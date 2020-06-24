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
        print("There is no Pattern in the scene.")
        return

    if not list(pattern.datastructure.vertices_where({'is_anchor': True})):
        print("Pattern has no anchor vertices! Please define anchor (support) vertices.")
        return

    form = FormDiagram.from_pattern(pattern.datastructure)
    form.edges_attribute('fmin', 0.1)
    form.vertices_attribute('is_fixed', False)
    fixed = list(pattern.datastructure.vertices_where({'is_fixed': True}))
    if fixed:
        form.vertices_attribute('is_anchor', True, keys=fixed)

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
