from compas_rv2.rhino import SubdObject
from compas_rhino.geometry import RhinoSurface
import compas_rhino

guid = compas_rhino.select_surface()
rhinosurface = RhinoSurface.from_guid(guid)
subdobject = SubdObject.from_rhinosurface(rhinosurface)
compas_rhino.rs.HideObject(guid)

print(subdobject.coarse)

# from compas.geometry import centroid_points_weighted
# from compas.geometry import centroid_points
# print('done')