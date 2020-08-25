from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .meshobject import MeshObject  # noqa: F401
from .skeletonobject import SkeletonObject  # noqa: F401
from .patternobject import PatternObject  # noqa: F401
from .formobject import FormObject  # noqa: F401
from .forceobject import ForceObject  # noqa: F401
from .thrustobject import ThrustObject  # noqa: F401


from compas_rv2.datastructures import Skeleton
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_rv2.datastructures import ThrustDiagram


MeshObject.register(Skeleton, SkeletonObject)
MeshObject.register(Pattern, PatternObject)
MeshObject.register(FormDiagram, FormObject)
MeshObject.register(ForceDiagram, ForceObject)
MeshObject.register(ThrustDiagram, ThrustObject)


__all__ = [name for name in dir() if not name.startswith('_')]
