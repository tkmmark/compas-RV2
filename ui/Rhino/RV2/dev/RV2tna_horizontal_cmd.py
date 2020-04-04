from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.geometry import Translation


__commandname__ = "RV2tna_horizontal"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    horizontal = proxy.package('compas_rv2.equilibrium.horizontal_nodal_proxy')

    form = scene.get('form')[0]
    force = scene.get('force')[0]

    if not form:
        return

    if not force:
        return

    kmax = scene.settings['tna.horizontal.kmax']
    alpha = scene.settings['tna.horizontal.alpha']

    options = ['alpha', 'kmax', 'ESC']
    while True:
        option = compas_rhino.rs.GetString('Options', options[-1], options)
        if not option or option == 'ESC':
            break

        if option == 'alpha':
            alpha_options = ['form{}'.format(int(i * 10)) for i in range(11)]
            temp = compas_rhino.rs.GetString('alpha', alpha_options[0], alpha_options)
            if not temp:
                alpha = 100
            else:
                alpha = int(temp[4:])

        elif option == 'kmax':
            kmax = compas_rhino.rs.GetString('kmax', kmax, 1, 10000)

    scene.settings['tna.horizontal.kmax'] = kmax
    scene.settings['tna.horizontal.alpha'] = alpha

    formdata, forcedata = horizontal(form.datastructure.data, force.datastructure.data, kmax=kmax, alpha=alpha)

    form.datastructure.data = formdata
    force.datastructure.data = forcedata

    bbox_form = form.datastructure.bounding_box_xy()
    bbox_force = force.datastructure.bounding_box_xy()
    xmin_form, xmax_form = bbox_form[0][0], bbox_form[1][0]
    xmin_force, _ = bbox_force[0][0], bbox_force[1][0]
    ymin_form, ymax_form = bbox_form[0][1], bbox_form[3][1]
    ymin_force, ymax_force = bbox_force[0][1], bbox_force[3][1]
    y_form = ymin_form + 0.5 * (ymax_form - ymin_form)
    y_force = ymin_force + 0.5 * (ymax_force - ymin_force)
    dx = 1.5 * (xmax_form - xmin_form) + (xmin_form - xmin_force)
    dy = y_form - y_force
    force.datastructure.transform(Translation([dx, dy, 0]))

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
