from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoSurface

__all__ = ['SubdObject']


class SubdObject(Object):
    def __init__(self):
        super(SubdObject, self).__init__()

# --------------------------------------------------------------------------
# constructors
# --------------------------------------------------------------------------
    def from_rhinosurface(cls):
        subdobject = cls()
        guid = compas_rhino.select_surface()
        rhinosurface = RhinoSurface.from_guid(guid)
        mesh = rhinosurface.brep_to_compas()
        