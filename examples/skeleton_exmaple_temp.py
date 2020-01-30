from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import RhinoSkeleton
import rhinoscriptsyntax as rs
from compas_rhino.utilities import objects

line_ids = rs.GetObjects("select curves", filter=rs.filter.curve)
lines = objects.get_line_coordinates(line_ids)
rs.DeleteObjects(line_ids)

skeleton = Skeleton.from_skeleton_lines(lines)
rhinoskeleton = RhinoSkeleton(skeleton)
rhinoskeleton.dynamic_draw_self()
rhinoskeleton.update()

skeleton.to_json('skeleton_temp2.json', pretty=True)
