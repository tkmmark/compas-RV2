from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas_rv2.datastructures.meshmixin import MeshMixin


__all__ = ['Pattern']


class Pattern(MeshMixin, Mesh):
    """Customised mesh data structure for RV2.

    Examples
    --------
    A :class:`Pattern` is used to define the geometry and boundary conditions of
    a funicular network in RV2.
    Patterns can be constructed from various inputs.

    >>> pattern = Pattern.from_lines()
    >>> pattern = Pattern.from_mesh()
    >>> pattern = Pattern.from_surface()
    >>> pattern = Pattern.from_skeleton()
    >>> pattern = Pattern.from_features()

    A pattern is essentially a mesh data structure, and therefore supports all operations
    available for meshes. For example,

    """

    def __init__(self, *args, **kwargs):
        super(Pattern, self).__init__(*args, **kwargs)
        self.default_vertex_attributes.update({
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'is_fixed': False,
        })
        self.default_edge_attributes.update({
            'q': 1.0,
            'lmin': 1e-6,
            'lmax': 1e6
        })

    # def collapse_small_edges(self, tol=1e-2):
    #     boundaries = self.vertices_on_boundaries()
    #     for boundary in boundaries:
    #         for u, v in pairwise(boundary):
    #             l = self.edge_length(u, v)
    #             if l < tol:
    #                 mesh_collapse_edge(self, v, u, t=0.5, allow_boundary=True)

    # def smooth(self, fixed, kmax=10):
    #     mesh_smooth_area(self, fixed=fixed, kmax=kmax)

    def relax(self):
        from compas.numerical import fd_numpy

        key_index = self.key_index()
        xyz = self.vertices_attributes('xyz')
        loads = [[0.0, 0.0, 0.0] for _ in xyz]
        fixed = [key_index[key] for key in self.vertices_where({'is_fixed': True})]
        edges = [(key_index[u], key_index[v]) for u, v in self.edges()]
        q = self.edges_attribute('q')

        xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

        for key in self.vertices():
            index = key_index[key]
            self.vertex_attributes(key, 'xyz', xyz[index])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
