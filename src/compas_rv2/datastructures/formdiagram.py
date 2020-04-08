from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import angle_vectors_xy
from compas.geometry import cross_vectors

from compas_tna.diagrams import FormDiagram
from compas_rv2.datastructures.meshmixin import MeshMixin


__all__ = ['FormDiagram']


class FormDiagram(MeshMixin, FormDiagram):
    """The RV2 FormDiagram.

    Examples
    --------
    The :class:`FormDiagram` is constructed from a :class:`Pattern`.
    The pattern defines the directions along which (horizontal) forces can flow
    through the funicular network.

    >>> form = FormDiagram.from_pattern(pattern)

    In order for the pattern to be valid input for making a form diagram,
    it should define both the geometry and the boundary conditions of the problem.
    """

    @classmethod
    def from_pattern(cls, pattern, feet=2):
        """Construct a form diagram from a pattern.

        Parameters
        ----------
        pattern : Pattern
            The pattern from which the diagram should be constructed.
        feet : {1, 2}, optional
            The number of horizontal force directions that should be added to the supports.

        Returns
        -------
        FormDiagram
            The form diagram.
        """
        form = pattern.copy(cls=cls)
        form.update_boundaries(feet=2)
        return form

    def dual_edge(self, key):
        """Get the corresponding edge in the ForceDiagram.

        Parameters
        ----------
        key : tuple
            The identifier of the edge in this diagram.

        Returns
        -------
        tuple
            The identifier of the edge in the other/dual diagram.

        Raises
        ------
        KeyError
            If the dual edge does not exist.
        """
        f1, f2 = key
        for u, v in self.dual.face_halfedges(f1):
            if self.dual.halfedge[v][u] == f2:
                return u, v

        raise KeyError(key)

    def update_angle_deviations(self):
        """Compute the angle deviation with the corresponding edge in the ForceDiagram.
        """
        for key in self.edges_where({'_is_external': False, '_is_edge': True}):
            uv = self.edge_vector(key[0], key[1])
            _key = self.dual_edge(key)
            _uv = self.dual.edge_vector(_key[0], _key[1])
            a = angle_vectors_xy(uv, cross_vectors((0, 0, 1), _uv), deg=True)
            self.edge_attribute(key, '_a', a)
            self.dual.edge_attribute(_key, '_a', a)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
