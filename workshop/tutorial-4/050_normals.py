import os
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bm_dual.json')

mesh = Mesh.from_json(FILE_I)
# mesh.flip_cycles()

artist = MeshArtist(mesh, layer="RV2::Dual")
artist.clear_layer()
artist.draw_faces()
artist.draw_vertexnormals(scale=1)
artist.redraw()
