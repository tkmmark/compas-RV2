from compas_rv2.rhino import SubdObject
from compas_rhino.geometry import RhinoSurface
import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

guid = compas_rhino.select_surface()
subdobject = SubdObject.from_guid(guid)
compas_rhino.rs.HideObject(guid)
subdobject.draw_coarse()
subdobject.get_default_strip_subdvision()
subdobject.get_subd()
subdobject.draw_subd()

subdobject.change_subd()
subdobject.draw_subd()

# subdobject.clear_subd()


# subdobject.draw_coarse()

# compas_rhino.rs.HideObject(guid)

# mesh.to_json('mesh_polysrf_5.json', pretty=True)

# mesh = Mesh.from_json('mesh_polysrf_5.json')
# artist = MeshArtist(mesh)
# # artist.draw_edges()
# # artist.draw_vertexlabels()
# edge = (16, 51)
# strip = edge_strip(mesh, edge)
# strips = edge_strips(mesh)
# print(strips)