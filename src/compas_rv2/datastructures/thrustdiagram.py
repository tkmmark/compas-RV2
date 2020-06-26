from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.datastructures.formdiagram import FormDiagram


__all__ = ['ThrustDiagram']


class ThrustDiagram(FormDiagram):
    """The RV2 ThrustDiagram."""

    def __init__(self, *args, **kwargs):
        super(ThrustDiagram, self).__init__(*args, **kwargs)
        self.attributes.update({
            'name': 'ThrustDiagram',
        })


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
