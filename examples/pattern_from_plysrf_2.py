import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas_rhino.geometry import RhinoSurface
from compas.datastructures import meshes_join_and_weld
from compas_rhino import select_mesh
from compas_rhino.geometry import RhinoMesh
from compas.datastructures import mesh_unify_cycles
# from compas.datastructures import mesh_split_edge
from copy import deepcopy
from compas.utilities import pairwise

# guids = compas_rhino.select_surfaces()
# density = 2, 2
# meshes = [RhinoSurface.from_guid(guid).uv_to_compas(density=density) for guid in guids]

# mesh = meshes_join_and_weld(meshes)
# mesh_unify_cycles(mesh)
# mesh.to_json('mesh_polysrf.json', pretty=True)


def mesh_split_edge(mesh, u, v, n=2):

    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    insert_keys = [u]
    for i in range(n)[1:]:
        t = 1/n * i

        # coordi= menates
        x, y, z = mesh.edge_point(u, v, t)

        # the split vertex
        w = mesh.add_vertex(x=x, y=y, z=z)
        insert_keys.append(w)

    insert_keys.append(v)
    # split half-edge UV
    for u, v in pairwise(insert_keys):
        mesh.halfedge[u][v] = fkey_uv

    del mesh.halfedge[u][v]

    # update the UV face if it is not the `None` face
    if fkey_uv is not None:
        j = mesh.face[fkey_uv].index(v)
        for w in insert_keys[::-1][1:-1]:
            mesh.face[fkey_uv].insert(j, w)

    # split half-edge VU
    for v, u in pairwise(insert_keys[::-1]):
        mesh.halfedge[v][u] = fkey_vu

    del mesh.halfedge[v][u]

    # update the VU face if it is not the `None` face
    if fkey_vu is not None:
        i = mesh.face[fkey_vu].index(u)
        for w in insert_keys[1:-1]:
            mesh.face[fkey_vu].insert(i, w)

    return insert_keys


def mesh_fast_copy(other):
    subd = Mesh()
    subd.vertex = deepcopy(other.vertex)
    subd.face = deepcopy(other.face)
    subd.facedata = deepcopy(other.facedata)
    subd.halfedge = deepcopy(other.halfedge)
    subd._max_int_key = other._max_int_key
    subd._max_int_fkey = other._max_int_fkey
    return subd


def mesh_subdivide_stripe(mesh, edge, k=1):
    pass


def edge_strip(mesh, uv):
    edges = []
    v, u = uv
    while True:
        edges.append((u, v))
        fkey = mesh.halfedge[u][v]
        if fkey is None:
            break
        vertices = mesh.face_vertices(fkey)
        if len(vertices) != 4:
            break
        i = vertices.index(u)
        u = vertices[i - 1]
        v = vertices[i - 2]
    edges[:] = [(u, v) for v, u in edges[::-1]]
    u, v = uv
    while True:
        fkey = mesh.halfedge[u][v]
        if fkey is None:
            break
        vertices = mesh.face_vertices(fkey)
        if len(vertices) != 4:
            break
        i = vertices.index(u)
        u = vertices[i - 1]
        v = vertices[i - 2]
        edges.append((u, v))
    return edges


mesh = Mesh.from_json('mesh_polysrf.json')

edges = edge_strip(mesh, (1, 9))

subd = mesh_fast_copy(mesh)

for u, v in edges:
    mesh_split_edge(subd, u, v, allow_boundary=True)

print(edges)


for u, v in edges:
    fkey = mesh.halfedge[u][v]
    if fkey is None:
        continue

    # add two faces
    face = subd.face[fkey]

    i = face.index(u)
    j = face.index(v)
    subd.add_face([u, face[(i+1) % 6], face[(i-2) % 6], face[(i-1) % 6]])
    subd.add_face([v, face[(j+1) % 6], face[(j+2) % 6], face[(j-1) % 6]])
    del subd.face[fkey]
    del subd.facedata[fkey]

# for u, v in edges:
#     fkey = mesh.halfedge[u][v]
#     if fkey is None:
#         continue

#     # add faces
#     face = subd.face[fkey]
#     n = len(face)
#     print(n)

#     i = face.index(u)
#     for w in range(int(n/2-1)):
#         print('a')
#         subd.add_face([face[i+w], face[(i+w+1) % n], face[(n-(i+w)) % n], face[(n-(i+w)+1) % n]])
#     del subd.face[fkey]
#     del subd.facedata[fkey]

# # mesh.to_json('mesh_polysrf_unify_split.json', pretty=True)
# subd.to_json('subd.json', pretty=True)

# guid = select_mesh()
# mesh = RhinoMesh.from_guid(guid).to_compas(cls=Mesh)
# mesh.to_json('mesh.json', pretty=True)

artist = MeshArtist(subd)
artist.draw_faces(join_faces=True)
artist.draw_vertexlabels()
