from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import RhinoSkeleton
# from compas_rv2.equilibrium import horizontal_nodal_proxy

from compas_rhino.utilities import objects
import rhinoscriptsyntax as rs
import time

from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_tna.rhino import DiagramHelper

from compas.rpc import Proxy

tna = Proxy('compas_tna.equilibrium')

# create rhino skeleton
line_ids = rs.GetObjects("select curves", filter=rs.filter.curve)
lines = objects.get_line_coordinates(line_ids)
rs.DeleteObjects(line_ids)

skeleton = Skeleton.from_skeleton_lines(lines)

rhinoskeleton = RhinoSkeleton(skeleton)
rhinoskeleton.dynamic_draw_self()
rhinoskeleton.update()

# construct form diagram
form = FormDiagram()
diagram_mesh = rhinoskeleton.diagram.to_diagram()

for key, attr in diagram_mesh.vertices(True):
    form.add_vertex(key, x=attr['x'], y=attr['y'], z=attr['z'])

for fkey in diagram_mesh.face:
    form.add_face(diagram_mesh.face[fkey])
form.draw(layer='TNA::FormDiagram', clear_layer=True)

keys = rhinoskeleton.diagram.to_support_vertices()

if keys:
    form.vertices_attributes(['is_anchor', 'is_fixed'], [True, True], keys=keys)
    form.draw(layer='TNA::FormDiagram', clear_layer=True)

form.update_boundaries(feet=2)
form.draw(layer='TNA::FormDiagram', clear_layer=True)

# force diagram
time.sleep(2)
force = ForceDiagram.from_formdiagram(form)
force.draw(layer='TNA::ForceDiagram', clear_layer=True)

if DiagramHelper.move(force):
    force.draw(layer='TNA::ForceDiagram', clear_layer=True)

# horizontal
time.sleep(2)


def horizontal(form, force, alpha=100, kmax=500):
    formdata, forcedata = tna.horizontal_nodal_proxy(form.to_data(), force.to_data(), alpha=alpha, kmax=kmax)
    # formdata, forcedata = horizontal_nodal_proxy(form.to_data(), force.to_data(), alpha=alpha, kmax=kmax)

    form.data = formdata
    force.data = forcedata


horizontal(form, force, alpha=100, kmax=500)
force.draw(layer='TNA::ForceDiagram', clear_layer=True)

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
