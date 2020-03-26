from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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
        form = pattern.copy(cls=cls)
        form.update_boundaries(feet=2)
        return form


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
