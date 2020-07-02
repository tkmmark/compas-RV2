import os
from compas.datastructures import Mesh
from compas_viewers.objectviewer import ObjectViewer

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bm_remeshed.ply')
FILE_O = os.path.join(HERE, 'bm_dual.json')

mesh = Mesh.from_ply(FILE_I)
dual = mesh.dual()

dual.to_json(FILE_O)

viewer = ObjectViewer()
viewer.add(dual, settings={'color': '#cccccc'})
viewer.update()
viewer.show()
