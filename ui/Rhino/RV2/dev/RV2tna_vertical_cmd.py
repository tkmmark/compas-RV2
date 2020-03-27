from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.geometry import subtract_vectors
from compas.geometry import length_vector


__commandname__ = "RV2tna_vertical"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    vertical = proxy.package('compas_tna.equilibrium.vertical_from_zmax_proxy')

    form = scene.get('form')[0]
    force = scene.get('force')[0]
    thrust = scene.get('thrust')[0]

    if not form:
        return

    if not force:
        return

    if not thrust:
        return

    bbox = form.datastructure.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox[2], bbox[0]))

    zmax = scene.settings['tna.vertical.zmax']
    kmax = scene.settings['tna.vertical.kmax']

    options = ['Zmax', 'Kmax', 'ESC']
    while True:
        option = compas_rhino.rs.GetString('Options', options[-1], options)
        if not option or option == 'ESC':
            break

        if option == 'Zmax':
            zmax = compas_rhino.rs.GetReal('Zmax', zmax, 0.1 * diagonal, 1.0 * diagonal)

        elif option == 'Kmax':
            kmax = compas_rhino.rs.GetString('Kmax', kmax, 1, 10000)

    scene.settings['tna.vertical.zmax'] = zmax
    scene.settings['tna.vertical.kmax'] = kmax

    formdata, scale = vertical(form.datastructure.data, zmax, kmax=kmax)

    force.datastructure.attributes['scale'] = scale
    form.datastructure.data = formdata
    thrust.datastructure.data = formdata

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
