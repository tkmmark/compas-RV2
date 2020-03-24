from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_tna.diagrams import FormDiagram
from compas_rv2.datastructures.meshmixin import MeshMixin


__all__ = ['FormDiagram']


class FormDiagram(MeshMixin, FormDiagram):
    """The RV2 FormDiagram.
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
