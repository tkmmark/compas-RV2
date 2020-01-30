from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import RhinoSkeleton
from compas_rhino.utilities import objects
import rhinoscriptsyntax as rs


line_ids = rs.GetObjects("select curves", filter=rs.filter.curve)
lines = objects.get_line_coordinates(line_ids)
rs.DeleteObjects(line_ids)

skeleton = Skeleton.from_skeleton_lines(lines)
# skeleton.leaf_width = 20
# skeleton.node_width = 20
# skeleton.update_mesh_vertices_pos()

rhinoskeleton = RhinoSkeleton(skeleton)
rhinoskeleton.dynamic_draw_self()
rhinoskeleton.update()

mesh = rhinoskeleton.diagram.to_diagram()
mesh.to_json('skeleton_temp1.json', pretty=True)
# rhinoskeleton.diagram.to_json('skeleton_temp1.json', pretty=True)

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
