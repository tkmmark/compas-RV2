import os
import json
from compas.utilities import DataDecoder
from compas_rv2.datastructures import FormDiagram
from compas_viewers.objectviewer import ObjectViewer

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bm-3.rv2')

with open(FILE_I, 'r') as f:
    session = json.load(f, cls=DataDecoder)

data = session['data']
form = FormDiagram.from_data(data['form'])

viewer = ObjectViewer()
viewer.add(form, settings={'color': '#cccccc'})
viewer.update()
viewer.show()
