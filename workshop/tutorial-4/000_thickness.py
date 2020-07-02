import os
import json
from compas.utilities import DataDecoder
from compas.utilities import DataEncoder
from compas.utilities import normalize_values
from compas_rv2.datastructures import FormDiagram

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bm-1.rv2')
FILE_O = os.path.join(HERE, 'bm-2.rv2')

with open(FILE_I, 'r') as f:
    session = json.load(f, cls=DataDecoder)

data = session['data']
form = FormDiagram.from_data(data['form'])

Tmin = 0.05
Tmax = 0.10

Z = form.vertices_attribute('z')
T = normalize_values(Z, Tmax, Tmin)

for index, vertex in enumerate(form.vertices()):
    form.vertex_attribute(vertex, 't', T[index])

session['data']['form'] = form.to_data()

with open(FILE_O, 'w') as f:
    json.dump(session, f, cls=DataEncoder)
