from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .scene import SceneNode  # noqa: F401
from .scene import Scene  # noqa: F401


# regisger wrappers for different diagrams
from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ForceDiagram
from compas_rv2.diagrams import ThrustDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoForceDiagram
from compas_rv2.rhino import RhinoThrustDiagram


Scene.register(FormDiagram, RhinoFormDiagram)
Scene.register(ForceDiagram, RhinoForceDiagram)
Scene.register(ThrustDiagram, RhinoThrustDiagram)


__all__ = [name for name in dir() if not name.startswith('_')]
