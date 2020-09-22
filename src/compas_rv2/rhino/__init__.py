"""
********************************************************************************
compas_rv2.rhino
********************************************************************************

.. currentmodule:: compas_rv2.rhino

Artists
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    FormArtist
    ForceArtist
    ThrustArtist

Forms
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

Objects
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    SkeletonObject
    PatternObject
    FormObject
    ForceObject
    ThrustObject

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.datastructures import Skeleton
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_rv2.datastructures import ThrustDiagram

from .helpers import *  # noqa: F401 F403
from .forms import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403
from .artists import MeshArtist
from .artists import FormArtist
from .artists import ForceArtist
from .artists import ThrustArtist
from .objects import *  # noqa: F401 F403
from .objects import MeshObject
from .objects import SkeletonObject
from .objects import PatternObject
from .objects import FormObject
from .objects import ForceObject
from .objects import ThrustObject
from .conduits import *  # noqa: F401 F403

MeshArtist.register(Skeleton, MeshArtist)
MeshArtist.register(Pattern, MeshArtist)
MeshArtist.register(FormDiagram, FormArtist)
MeshArtist.register(ForceDiagram, ForceArtist)
MeshArtist.register(ThrustDiagram, ThrustArtist)

MeshObject.register(Skeleton, SkeletonObject)
MeshObject.register(Pattern, PatternObject)
MeshObject.register(FormDiagram, FormObject)
MeshObject.register(ForceDiagram, ForceObject)
MeshObject.register(ThrustDiagram, ThrustObject)


__all__ = [name for name in dir() if not name.startswith('_')]
