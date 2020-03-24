from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_tna.diagrams import ThrustDiagram
from compas_rv2.datastructures.meshmixin import MeshMixin
from compas_rv2.datastructures.formdiagram import FormDiagram
from compas_rv2.datastructures.forcediagram import ForceDiagram


__all__ = ['ThrustDiagram']


# make the thrust diagram the main diagram
# it has a horizontal projection, the form diagram,
# with its reciprocal, the (horizontal) force diagram

# a thrust diagram has the 3D geometry of the pattern
# from which it is constructed
# if so desired, it can be used as the target during form finding
# note: how to keep the target fixed if the diagram itself changes? => zT?
# note: if the xy of the thrust diagram are allowed to change, zT have to be resampled when they do...

class ThrustDiagram(MeshMixin, FormDiagram):
    """The RV2 ThrustDiagram.

    Examples
    --------
    In RV2, a ThrustDiagram is created from a Pattern.
    From the information contained in the pattern, a form and froce diagram are initialised.

    >>> thrust = ThrustDiagram.from_pattern(pattern)
    """

    def __init__(self, *args, **kwargs):
        super(ThrustDiagram, self).__init__(*args, **kwargs)
        self.form = None
        self.force = None

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
        form = FormDiagram.from_mesh(pattern)
        form.vertices_attribute('z', 0.0)
        form.update_boundaries(feet=feet)
        force = ForceDiagram.from_formdiagram(form)
        thrust = cls.from_mesh(pattern)
        thrust.form = form
        thrust.force = force
        return thrust


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
