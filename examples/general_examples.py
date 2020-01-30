# from __future__ import print_function
# from __future__ import absolute_import
# from __future__ import division

# from compas_rv2.datastructures import Skeleton
# from compas_rv2.rhino import RhinoSkeleton
# import compas_rhino

# from compas_rhino.utilities import objects
# import rhinoscriptsyntax as rs

# guids = compas_rhino.select_lines()
# lines = compas_rhino.get_line_coordinates(guids)
# skeleton = Skeleton.from_skeleton_lines(lines)
# rhinoskeleton = RhinoSkeleton(skeleton)
# rhinoskeleton.move_diagram_vertex

# import Rhino
# import System
# # gp = GetPoint()
# gp = Rhino.Input.Custom.GetPoint()
# gp.SetCommandPrompt("Pick a point")
# # gp.SetCursor(System.Windows.Forms.Cursors.Hand)
# gp.SetCursor(Rhino.UI.CursorStyle.Default)
# # gp.SetCursor(0)

# gp.Get()

from System.Windows.Forms import Cursor, Cursors
import rhinoscriptsyntax as rs

# # Turn on the waiting or busy cursor symbol
# Cursor.Current = Cursors.WaitCursor
# rs.Sleep(1000)
# # Turn on the waiting or busy cursor symbol
# Cursor.Current = Cursors.Hand
# rs.Sleep(1000)

# # reset cursor
# Cursor.Current = Cursors.Default
import Rhino

gs = Rhino.Input.Custom.GetString()
gs.AcceptNothing(True)
message = 'test'
strings = ['a', 'b']
gs.SetCommandPrompt(message)

if strings:
    for s in strings:
        gs.AddOption(s)
result = gs.Get()
# if result==Rhino.Input.GetResult.Cancel: return None
# if( result == Rhino.Input.GetResult.Option ):
#     return gs.Option().EnglishName
print(gs.StringResult())
