from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import RhinoSkeleton

skeleton = Skeleton.from_json('skeleton_temp1.json')
rhinoskeleton = RhinoSkeleton(skeleton)
rhinoskeleton.dynamic_draw_self()
