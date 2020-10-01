import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas_rhino.geometry import RhinoSurface
from compas.datastructures import meshes_join_and_weld
from compas_rhino import select_mesh
from compas_rhino.geometry import RhinoMesh
from compas.datastructures import mesh_unify_cycles
from copy import deepcopy
from compas.utilities import pairwise
import Rhino

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


def edge_strips(mesh):
    edges = list(mesh.edges())

    strips = {}
    index = -1
    while len(edges) > 0:
        index += 1
        u0, v0 = edges.pop()
        strip = edge_strip(mesh, (u0, v0))
        strips.update({index: strip})

        for u, v in strip:
            if (u, v) in edges:
                edges.remove((u, v))
            elif (v, u) in edges:
                edges.remove((v, u))

    return(strips)


def mesh_split_edges(mesh, edges, n):
    subd = mesh_fast_copy(mesh)
    for u, v in edges:
        mesh_split_edge(subd, u, v, n)

    return subd


def mesh_sbudivide_strip(mesh, uv, n):

    edges = edge_strip(mesh, uv)
    subd = mesh_split_edges(mesh, edges, n)

    for u, v in edges:
        fkey = mesh.halfedge[u][v]
        if fkey is None:
            continue

        # add faces
        face = subd.face[fkey]
        n = len(face)
        i = face.index(u)

        for w in range(int(n/2-1)):
            subd.add_face([face[(w+i) % n], face[(w+1+i) % n], face[(n-w-2+i) % n], face[(n-w-1+i) % n]])

        del subd.face[fkey]
        del subd.facedata[fkey]

    return subd

guid = compas_rhino.select_surface()
rhinosrf = RhinoSurface.from_guid(guid)
mesh = rhinosrf.brep_to_compas()
compas_rhino.rs.HideObject(guid)

# artist = MeshArtist(mesh)
# artist.draw_faces(join_faces=True)
# artist.draw_vertexlabels()
# mesh.to_json('mesh_polysrf_3.json', pretty=True)

# mesh = Mesh.from_json('mesh_polysrf_3.json')
artist = MeshArtist(mesh)
guids = artist.draw_edges()
guid_edge = {guid: edge for guid, edge in zip(guids, list(mesh.edges()))}
artist.redraw()

# # divide all edges into target length, draw a temp view
# target_length = compas_rhino.rs.GetReal('target edge length?')
# strips = edge_strips(mesh)
# for i, edges in strips.items():
#     edge0 = edges.pop()
#     n = int(round(mesh.edge_length(edge0[0], edge0[1]) / target_length))
#     mesh_temp = mesh_sbudivide_strip(mesh, edge0, n)

# compas_rhino.delete_objects(guids, purge=True)
# artist_temp = MeshArtist(mesh_temp)
# guids_temp = artist_temp.draw_edges()
# guid_edge_temp = {guid: edge for guid, edge in zip(guids_temp, list(mesh_temp.edges()))}
# artist_temp.redraw()

# customize the subdivision for choosen strip
while True:

    guid = compas_rhino.select_lines('select the edge to be redivided')
    if not guid:
        break

    edge = guid_edge[guid[0]]
    n = compas_rhino.rs.GetInteger('divide into?')
    mesh = mesh_sbudivide_strip(mesh, edge, n)

    compas_rhino.delete_objects(guids, purge=True)
    artist = MeshArtist(mesh)
    guids = artist.draw_edges()
    guid_edge = {guid: edge for guid, edge in zip(guids, list(mesh.edges()))}
    artist.redraw()


# artist.draw_vertexlabels()
# artist.draw_faces(join_faces=True)
# artist.draw_vertexlabels()
