from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.objects import BaseObject

__all__ = ['SubdObject']


class SubdObject(BaseObject):
    def __init__(self, coarse, scene=None, name=None, layer=None, visible=True, settings=None):
        super(SubdObject, self).__init__(coarse, scene, name, layer, visible)
        self._guids = []
        self._guid_coarse_vertex = {}
        self._guid_coarse_edge = {}
        self._guid_subd_vertex = {}
        self._guid_subd_edge = {}
        self._guid_subd_face = {}
        self._guid_subd = {}
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self.settings.update(type(self).SETTINGS)
        if settings:
            self.settings.update(settings)

# --------------------------------------------------------------------------
# properties
# --------------------------------------------------------------------------
    @property
    def coarse(self):
        return self.item

    @coarse.setter
    def coarse(self, coarse):
        self.item = coarse
        self._guids = []
        self._guid_coarse_vertex = {}
        self._guid_coarse_edge = {}
        self._guid_subd_vertex = {}
        self._guid_subd_edge = {}
        self._guid_subd_face = {}
        self._guid_subd = {}

# --------------------------------------------------------------------------
# constructors
# --------------------------------------------------------------------------

    def from_rhinosurface(self, rhinosurface):
        self.coarse = rhinosurface.brep_to_compas()
        