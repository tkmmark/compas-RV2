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

    >>> force = FroceDiagram.from_formdiagram(form)
    """

    def primal_edge(self, key):
        """Get the corresponding edge in the FormDiagram.

        Parameters
        ----------
        key : tuple
            The identifier of the edge in this diagram.

        Returns
        -------
        tuple
            The identifier of the edge in the other/primal diagram.

        Raises
        ------
        KeyError
            If the dual edge does not exist.

        """
        f1, f2 = key
        for u, v in self.primal.face_halfedges(f1):
            if self.primal.halfedge[v][u] == f2:
                return u, v
        raise KeyError(key)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
