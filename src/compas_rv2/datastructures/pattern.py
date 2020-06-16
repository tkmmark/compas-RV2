from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas.datastructures import mesh_smooth_area
from compas_rv2.datastructures.meshmixin import MeshMixin

from compas_singular.algorithms import boundary_triangulation
from compas_singular.algorithms import SkeletonDecomposition


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
        self.attributes.update({
            'openings': {}
        })
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

    @classmethod
    def from_features(cls, target_length, outer_boundary, inner_boundaries=[], polyline_features=[], point_features=[]):
        """Get a pattern object from a set of planar polylines.
        The outer boundary is mandatory and the inner boundaries, polyline and point features are optional.
        The discretisation of the polylines dictates the accuracy of the underlying triangulation and therefore of the resulting decomposition. Values between 1% and 5% of the length of the diagonal of the bounding box are recommended.
        The pattern is aligned to the curves (boundary polylines and feature polylines).
        The pattern contains a pole singularity at the feature points. Pole singularities are a specific type of singularity.

        Parameters
        ----------
        target_length : float
            The edge target length for densification.
        outer_boundary : list
            One list of point coordinates discretising the outer boundary.
        inner_boundaries : list, []
            Optional. A list of lists of point coordinates discretising each inner boundary.
        polyline_features : list, []
            Optional. A list of lists of point coordinates discretising each feature polyline. WIP
        point_features : list, []
            Optional. A list of point coordinates at the location of pole singularities.

        Returns
        -------
        Pattern
            A Pattern object.

        Examples
        --------
        >>> import json
        >>> from compas_plotters.meshplotter import MeshPlotter
        >>> filepath = '../../../data/pattern_from_features.json'
        >>> with open(filepath, 'r') as fp:
        >>>     data = json.load(fp)
        >>> outer_boundary, inner_boundaries, polyline_features, point_features = data
        >>> pattern = Pattern.from_features(.25, outer_boundary, inner_boundaries, polyline_features, point_features)
        >>> plotter = MeshPlotter(pattern, figsize=(5, 5))
        >>> plotter.draw_edges(width=.1)
        >>> plotter.draw_faces()
        >>> plotter.show()

        References
        ----------
        Based on [1]_ and [2]_.

        .. [1] Oval et al. *Feature-based topology finding of patterns for shell structures*. Automation in Construction, 2019.
               Available at: https://www.researchgate.net/publication/331064073_Feature-based_Topology_Finding_of_Patterns_for_Shell_Structures.
        .. [2] Oval. *Topology finding of patterns for structural design*. PhD thesis, Unversité Paris-Est, 2019.
               Available at: https://www.researchgate.net/publication/340096530_Topology_Finding_of_Patterns_for_Structural_Design.

        """        

        tri_mesh = boundary_triangulation(outer_boundary, inner_boundaries, polyline_features, point_features, src='numpy')
        decomposition = SkeletonDecomposition.from_mesh(tri_mesh)
        coarse_mesh = decomposition.decomposition_mesh(point_features)

        coarse_mesh.collect_strips()
        coarse_mesh.set_strips_density_target(target_length)
        coarse_mesh.densification()

        dense_mesh = coarse_mesh.get_quad_mesh()
        vertices, faces = dense_mesh.to_vertices_and_faces()
        return cls.from_vertices_and_faces(vertices.values(), faces.values())

    def collapse_small_edges(self, tol=1e-2):
        for key in list(self.edges()):
            if self.has_edge(key):
                u, v = key
                l = self.edge_length(u, v)
                if l < tol:
                    mesh_collapse_edge(self, u, v, t=0.5, allow_boundary=True)

    def smooth(self, fixed, kmax=10):
        mesh_smooth_area(self, fixed=fixed, kmax=kmax)

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
    import json
    from compas_plotters.meshplotter import MeshPlotter
    filepath = '../../../data/pattern_from_features.json'
    with open(filepath, 'r') as fp:
        data = json.load(fp)
    outer_boundary, inner_boundaries, polyline_features, point_features = data
    pattern = Pattern.from_features(.25, outer_boundary, inner_boundaries, polyline_features, point_features)
    plotter = MeshPlotter(pattern, figsize=(5, 5))
    plotter.draw_edges(width=.1)
    plotter.draw_faces()
    plotter.show()
