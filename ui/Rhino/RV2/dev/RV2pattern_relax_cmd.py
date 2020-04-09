from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2pattern_relax"


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

    if not list(pattern.datastructure.vertices_where({'is_fixed': True})):
        print("Pattern has No fixed vertices! ")
        return

    bq = 5
    iq = 1

    options = ['boundary_edges', 'interior_edges']
    while True:
        option = compas_rhino.rs.GetString('Enter qs for edges', strings=options)

        if not option:
            break

        if option == 'boundary_edges':
            bq = compas_rhino.rs.GetReal('q for boundary edges', bq, 0.1, 10)

        if option == 'interior_edges':
            iq = compas_rhino.rs.GetReal('q for interior edges', iq, 0.1, 10)

    relax = proxy.package("compas.numerical.fd_numpy")

    # update fixed vertices
    # update "sag" of resulting boundary openings
    # run fd

    key_index = pattern.datastructure.key_index()
    xyz = pattern.datastructure.vertices_attributes('xyz')
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed = [key_index[key] for key in pattern.datastructure.vertices_where({'is_fixed': True})]
    edges = [(key_index[u], key_index[v]) for u, v in pattern.datastructure.edges()]

    q = []
    for key in pattern.datastructure.edges():
        if pattern.datastructure.is_edge_on_boundary(*key):
            q.append(bq)
        else:
            q.append(iq)

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
