"""
********************************************************************************
compas_rv2.scene
********************************************************************************

.. currentmodule:: compas_rv2.scene


.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .scene import Scene

from compas_rv2.datastructures import Skeleton
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_rv2.datastructures import ThrustDiagram

from compas_rv2.rhino import SkeletonObject
from compas_rv2.rhino import PatternObject
from compas_rv2.rhino import FormObject
from compas_rv2.rhino import ForceObject
from compas_rv2.rhino import ThrustObject


Scene.register(Skeleton, SkeletonObject)
Scene.register(Pattern, PatternObject)
Scene.register(FormDiagram, FormObject)
Scene.register(ForceDiagram, ForceObject)
Scene.register(ThrustDiagram, ThrustObject)


__all__ = [name for name in dir() if not name.startswith('_')]
