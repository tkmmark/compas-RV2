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
    In RV2, a FormDiagram is created from a Pattern.
    The Pattern contains all information to be able to initialise the form diagram
    and update its boundaries.

    >>> form = FormDiagram.from_pattern(pattern)
    """

    @classmethod
    def from_pattern(cls, pattern, feet=2):
        """Construct a FormDiagram from a Pattern.

        Parameters
        ----------
        pattern : :class:`compas_rv2.datastructures.Pattern`
            The input pattern.
        feet : {1, 2}, optional
            The number of feet to be added to the anchor vertices.

        Returns
        -------
        :class:`compas_rv2.datastructures.FormDiagram`
            The form diagram.
        """
        form = cls.from_mesh(pattern)
        form.update_boundaries(feet=feet)
        return form


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
