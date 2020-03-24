from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2pattern_smooth"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    relax = proxy.package("compas.numerical.fd_numpy")

    key_index = pattern.datastructure.key_index()
    xyz = pattern.datastructure.vertices_attributes('xyz')
    loads = pattern.datastructure.vertices_attributes(['px', 'py', 'pz'])
    fixed = [key_index[key] for key in pattern.datastructure.vertices_where({'is_fixed': True})]
    edges = [(key_index[u], key_index[v]) for u, v in pattern.edges()]
    q = pattern.datastructure.edges_attribute('q')

    xyz, q, f, l, r = relax(xyz, edges, fixed, q, loads)

    for key in pattern.datastructure.vertices():
        index = key_index[key]
        pattern.datastructure.vertex_attributes(key, 'xyz', xyz[index])

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
