from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import RhinoSkeleton
from compas_rhino.utilities import objects
import rhinoscriptsyntax as rs


line_ids = rs.GetObjects("select curves", filter=rs.filter.curve)
lines = objects.get_line_coordinates(line_ids)
# rs.DeleteObjects(line_ids)

skeleton = Skeleton.from_skeleton_lines(lines)

rhinoskeleton = RhinoSkeleton(skeleton)
rhinoskeleton.dynamic_draw_self()

rhinoskeleton.update_in_rhino()

"""
update function should be embeded in UI.
following functions are available:

    'move_skeleton'
    'move_diagram'
    'leaf_width'
    'node_width'
    'subdivide'
    'merge'
    'add_lines'
    'remove_lines'
    'export'
    'stop'
"""

rhinoskeleton.diagram.to_json('skeleton_temp1.json', pretty=True)
