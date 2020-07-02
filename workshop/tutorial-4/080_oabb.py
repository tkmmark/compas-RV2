import os
import json
from compas.datastructures import Mesh
from compas.geometry import Frame, Transformation
from compas_rhino.artists import MeshArtist
from compas_cloud import Proxy
from compas_rv2.rhino import ErrorHandler

errorHandler = ErrorHandler(title="Server side Error", showLocalTraceback=False)
proxy = Proxy(errorHandler=errorHandler, background=False)
pca = proxy.function('compas.numerical.pca_numpy')

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'blocks.json')

with open(FILE_I, 'r') as f:
    blocks = [Mesh.from_data(data) for data in json.load(f)]

world = Frame.worldXY()

for block in blocks:
    points = block.vertices_attributes('xyz')
    point, axes, _ = pca(points)
    frame = Frame(point, axes[0], axes[1])
    X = Transformation.from_frame_to_frame(frame, world)
    block.transform(X)

artist = MeshArtist(None, layer="RV2::XBlocks")
artist.clear_layer()

for block in blocks:
    artist.mesh = block
    artist.draw_faces(color=(0, 255, 255), join_faces=True)

artist.redraw()
