import compas
from compas.utilities import pairwise
from compas.utilities import i_to_green
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_plotters import MeshPlotter

# ==============================================================================
# Patterning
#
# base relaxation on definition of sag values
# provide alternative solution using "pushed out" force diagram vertices
# ==============================================================================

pattern = Pattern.from_obj(compas.get('faces.obj'))

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

pattern.edges_attribute('q', 3.0, keys=e1)
pattern.edges_attribute('q', 7.0, keys=e3)

pattern.relax()

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
plotter.show()

# angles = []
# for edge in force.edges():
#     _edge = force.primal_edge(edge)
#     a = form.edge_attribute(_edge, '_a')
#     angles.append(a)

# amin = min(angles)
# amax = max(angles)

# edgelabel = {}
# for edge in force.edges():
#     _edge = force.primal_edge(edge)
#     a = form.edge_attribute(_edge, '_a')
#     if a > 1:
#         edgelabel[edge] = "{:.1f}".format(a)

# visualize force
plotter = MeshPlotter(force, figsize=(8, 5))
plotter.draw_edges()
plotter.show()
