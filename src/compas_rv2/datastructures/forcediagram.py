from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_tna.diagrams import ForceDiagram
from compas_rv2.datastructures.meshmixin import MeshMixin


__all__ = ['ForceDiagram']


class ForceDiagram(MeshMixin, ForceDiagram):
    """The RV2 ForceDiagram.

    Examples
    --------
    The :class:`ForceDiagram` is constructed from the :class:`FormDiagram` using
    :func:`ForceDiagram.from_formdiagram`. In RV2 this is dones as part of the
    TNA initialisation process.

    >>> form = FormDiagram.from_pattern(pattern)
    >>> force = FroceDiagram.from_formdiagram(form)

    Note that these two diagrams are dual, but not reciprocal.
    To make them reciprocal, run :func:`horizontal_nodal_proxy`.
    """


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
