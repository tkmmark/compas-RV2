from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from .scene import SceneNode  # noqa: F401
from .scene import Scene

from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ForceDiagram
from compas_rv2.diagrams import ThrustDiagram
from compas_rv2.skeleton import Skeleton
from compas_rv2.patterns import Pattern

from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoForceDiagram
from compas_rv2.rhino import RhinoThrustDiagram
from compas_rv2.rhino import RhinoSkeleton
from compas_rv2.rhino import PatternObject


Scene.register(FormDiagram, RhinoFormDiagram)
Scene.register(ForceDiagram, RhinoForceDiagram)
Scene.register(ThrustDiagram, RhinoThrustDiagram)
Scene.register(Skeleton, RhinoSkeleton)

Scene.register(Pattern, PatternObject)


__all__ = [name for name in dir() if not name.startswith('_')]
