from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas_rv2.datastructures.meshmixin import MeshMixin


__all__ = ['Pattern']


class Pattern(MeshMixin, Mesh):
    """Customised mesh data structure for RV2."""

    def __init__(self, *args, **kwargs):
        super(Pattern, self).__init__(*args, **kwargs)
        self.default_vertex_attributes.update({
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'is_fixed': False,
            'is_anchor': False
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
