from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.datastructures.formdiagram import FormDiagram


__all__ = ['ThrustDiagram']


# make the thrust diagram the main diagram
# it has a horizontal projection, the form diagram,
# with its reciprocal, the (horizontal) force diagram

# a thrust diagram has the 3D geometry of the pattern
# from which it is constructed
# if so desired, it can be used as the target during form finding
# note: how to keep the target fixed if the diagram itself changes? => zT?
# note: if the xy of the thrust diagram are allowed to change, zT have to be resampled when they do...

class ThrustDiagram(FormDiagram):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
