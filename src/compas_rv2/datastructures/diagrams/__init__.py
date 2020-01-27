from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from .formdiagram import FormDiagram
from .forcediagram import ForceDiagram

if not compas.IPY:
    from .relax_numpy import relax_boundary_openings_numpy

    def relax_boundary_openings_proxy(formdata, fixed):
        form = FormDiagram.from_data(formdata)
        relax_boundary_openings_numpy(form, fixed)
        return form.to_data()


__all__ = [name for name in dir() if not name.startswith('_')]
