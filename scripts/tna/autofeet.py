import compas
from compas.utilities import pairwise
from compas.utilities import i_to_green
from compas.geometry import distance_point_point_xy
from compas.geometry import intersection_line_line_xy
from compas.geometry import midpoint_point_point_xy
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_plotters import MeshPlotter


def compute_sag(edges):
    u, v = edges[0]
    if pattern.vertex_attribute(u, 'is_fixed'):
        a = pattern.vertex_attributes(u, 'xyz')
        aa = pattern.vertex_attributes(v, 'xyz')
    else:
        a = pattern.vertex_attributes(v, 'xyz')
        aa = pattern.vertex_attributes(u, 'xyz')
    u, v = edges[-1]
    if pattern.vertex_attribute(u, 'is_fixed'):
        b = pattern.vertex_attributes(u, 'xyz')
        bb = pattern.vertex_attributes(v, 'xyz')
    else:
        b = pattern.vertex_attributes(v, 'xyz')
        bb = pattern.vertex_attributes(u, 'xyz')
    span = distance_point_point_xy(a, b)
    apex = intersection_line_line_xy((a, aa), (b, bb))
    midspan = midpoint_point_point_xy(a, b)
    rise = 0.5 * distance_point_point_xy(midspan, apex)
    sag = rise / span
    return sag


# ==============================================================================
# Patterning
#
# base relaxation on definition of sag values
# provide alternative solution using "pushed out" force diagram vertices
# ==============================================================================

pattern = Pattern.from_obj(compas.get('faces.obj'))

lines = []
for u, v in pattern.edges():
    lines.append({
        'start': pattern.vertex_coordinates(u),
        'end': pattern.vertex_coordinates(v),
        'color': '#cccccc',
    })

# modify pattern
# - fix vertices
# - relax boundaries
pattern.vertices_attribute('is_fixed', True, keys=list(pattern.vertices_where({'vertex_degree': 2})))

vertices = pattern.continuous_vertices_on_boundary((0, 6))  # add breakpoints as optional argument
pattern.vertices_attribute('is_fixed', True, keys=vertices)

vertices = pattern.continuous_vertices_on_boundary((5, 11))  # add breakpoints as optional argument
pattern.vertices_attribute('is_fixed', True, keys=vertices)

e1 = list(pairwise(pattern.continuous_vertices_on_boundary((0, 1))))
e3 = list(pairwise(pattern.continuous_vertices_on_boundary((30, 31))))

target1 = 0.15
q1 = 10  # set equal to the length of the corresponding edge of the boundary polygon

target2 = 0.2
q2 = 10  # set equal to the length of the corresponding edge of the boundary polygon

pattern.edges_attribute('q', q1, keys=e1)
pattern.edges_attribute('q', q2, keys=e3)

pattern.relax()

while True:
    sag1 = compute_sag(e1)
    sag2 = compute_sag(e3)

    if (sag1 - target1)**2 < 0.001**2 and (sag2 - target2)**2 < 0.001**2:
        break

    q1 = sag1 / target1 * q1
    q2 = sag2 / target2 * q2

    pattern.edges_attribute('q', q1, keys=e1)
    pattern.edges_attribute('q', q2, keys=e3)
    pattern.relax()

print(q1)
print(q2)

# define boundary conditions
# - identify suppports
# - define loads (these can still be updated later)
pattern.vertices_attribute('is_anchor', True, keys=list(pattern.vertices_where({'is_fixed': True})))

# ==============================================================================
# TNA
# ==============================================================================

# create form diagram
form = FormDiagram.from_pattern(pattern)
force = ForceDiagram.from_formdiagram(form)

# horizontal equilibrium
horizontal_nodal(form, force, kmax=100)

# ==============================================================================
# Visualization
# ==============================================================================

angles = form.edges_attribute('_a', keys=list(form.edges_where({'_is_edge': True})))
amin = min(angles)
amax = max(angles)

edgelabel = {}
for edge in form.edges_where({'_is_edge': True}):
    a = form.edge_attribute(edge, '_a')
    if a > 3:
        edgelabel[edge] = "{:.1f}".format(a)

# visualize form
plotter = MeshPlotter(form, figsize=(8, 5))
plotter.draw_vertices(
    facecolor={key: (255, 0, 0) for key in form.vertices_where({'is_anchor': True})}
)
plotter.draw_edges(
    text=edgelabel,
    keys=list(form.edges_where({'_is_edge': True})),
    color=dict((key, (0, 0, 255)) for key in form.edges_where({'_is_external': True})),
    fontsize=6
)
plotter.draw_faces(
    # text="key",
    keys=list(form.faces_where({'_is_loaded': True}))
)
plotter.draw_lines(lines)
plotter.show()

# # angles = []
# # for edge in force.edges():
# #     _edge = force.primal_edge(edge)
# #     a = form.edge_attribute(_edge, '_a')
# #     angles.append(a)

# # amin = min(angles)
# # amax = max(angles)

# # edgelabel = {}
# # for edge in force.edges():
# #     _edge = force.primal_edge(edge)
# #     a = form.edge_attribute(_edge, '_a')
# #     if a > 1:
# #         edgelabel[edge] = "{:.1f}".format(a)

# # visualize force
# plotter = MeshPlotter(force, figsize=(8, 5))
# plotter.draw_edges()
# plotter.show()
