from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.geometry import subtract_vectors
from compas.geometry import length_vector


__commandname__ = "RV2tna_vertical"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    vertical = proxy.function('compas_tna.equilibrium.vertical_from_zmax_proxy')

    form = scene.get('form')[0]
    force = scene.get('force')[0]
    thrust = scene.get('thrust')[0]

    if not form:
        print("There is no FormDiagram in the scene.")
        return

    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    bbox = form.datastructure.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox[2], bbox[0]))

    zmax = scene.settings['tna.vertical.zmax']
    kmax = scene.settings['tna.vertical.kmax']

    options = ['target_height', 'iterations']

    while True:
        option = compas_rhino.rs.GetString('Options for vertical equilibrium solver:', strings=options)

        if not option:
            break

        elif option == 'target_height':
            zmax = compas_rhino.rs.GetReal('Enter target height of the ThrustDiagram', zmax, 0.1 * diagonal, 1.0 * diagonal)

        elif option == 'iterations':
            kmax = compas_rhino.rs.GetInteger('Enter number of iterations', 100, 1, 10000)

    scene.settings['tna.vertical.zmax'] = zmax
    scene.settings['tna.vertical.kmax'] = kmax

    formdata, scale = vertical(form.datastructure.data, zmax, kmax=kmax)

    force.settings['show.color.analysis'] = form.settings['show.color.analysis']
    force.settings['tol.angles'] = form.settings['tol.angles']

    force.datastructure.attributes['scale'] = scale
    form.datastructure.data = formdata
    thrust.datastructure.data = formdata

    scene.update()

    print('Vertical equilibrium found!')
    print('ThrustDiagram object successfully created.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
