import compas
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_plotters import MeshPlotter

pattern = Pattern.from_obj(compas.get('faces.obj'))

# modify pattern
# - fix vertices
# - relax boundaries
pattern.vertices_attribute('is_fixed', True, keys=list(pattern.vertices_where({'vertex_degree': 2})))

vertices = pattern.continuous_vertices_on_boundary((0, 6))
pattern.vertices_attribute('is_fixed', True, keys=vertices)

# define boundary conditions
# - identify suppports
# - define loads (these can still be updated later)
pattern.vertices_attribute('is_anchor', True, keys=list(pattern.vertices_where({'is_fixed': True})))

# create form diagram
form = FormDiagram.from_pattern(pattern)

# visualize
plotter = MeshPlotter(form, figsize=(8, 5))
plotter.draw_vertices(
    # text="key",
    # radius=0.2,
    facecolor={key: (255, 0, 0) for key in form.vertices_where({'is_anchor': True})})
plotter.draw_edges(
    keys=list(form.edges_where({'_is_edge': True})),
    color=dict((key, (0, 0, 255)) for key in form.edges_where({'_is_external': True})))
plotter.draw_faces(keys=list(form.faces_where({'_is_loaded': True})))
plotter.show()
