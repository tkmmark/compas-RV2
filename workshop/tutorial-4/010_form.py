import os
import json
from compas.utilities import DataDecoder
from compas_rv2.datastructures import FormDiagram
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bm-3.rv2')
FILE_O = os.path.join(HERE, 'form.json')

with open(FILE_I, 'r') as f:
    session = json.load(f, cls=DataDecoder)

data = session['data']
form = FormDiagram.from_data(data['form'])
form.to_json(FILE_O)

artist = MeshArtist(form, layer="RV2::Mesh")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.redraw()
