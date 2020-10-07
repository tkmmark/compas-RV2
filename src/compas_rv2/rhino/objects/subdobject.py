from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.objects import BaseObject
from compas_rhino.artists import MeshArtist
from compas_rhino.geometry import RhinoSurface
from compas_rhino import delete_objects
from compas.datastructures import Mesh
from compas.utilities import pairwise
from copy import deepcopy
import rhinoscriptsyntax as rs

__all__ = ['SubdObject']


def mesh_fast_copy(other):
    subd = Mesh()
    subd.vertex = deepcopy(other.vertex)
    subd.face = deepcopy(other.face)
    subd.facedata = deepcopy(other.facedata)
    subd.halfedge = deepcopy(other.halfedge)
    subd._max_face = other._max_face
    subd._max_vertex = other._max_vertex
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

    return strips


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
    for a, b in pairwise(insert_keys):
        mesh.halfedge[a][b] = fkey_uv

    del mesh.halfedge[u][v]

    # update the UV face if it is not the `None` face
    if fkey_uv is not None:
        j = mesh.face[fkey_uv].index(v)
        for w in insert_keys[::-1][1:-1]:
            mesh.face[fkey_uv].insert(j, w)

    # split half-edge VU
    for b, a in pairwise(insert_keys[::-1]):
        mesh.halfedge[b][a] = fkey_vu

    del mesh.halfedge[v][u]

    # update the VU face if it is not the `None` face
    if fkey_vu is not None:
        i = mesh.face[fkey_vu].index(u)
        for w in insert_keys[1:-1]:
            mesh.face[fkey_vu].insert(i, w)

    return insert_keys


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


class SubdObject(BaseObject):

    SETTINGS = {
        'layer': "RV2::Subd",
        'color.vertices': (255, 255, 255),
        'color.edges': (0, 0, 0),
        'color.faces': (0, 0, 0),
        'color.mesh': (0, 0, 0),
        'color.subd.edges': (100, 100, 100),
        'show.mesh': True,
        'show.vertices': True,
        'show.edges': True,
        'show.faces': False,
    }

    def __init__(self, coarse=None, scene=None, name=None, layer=None, visible=True, settings=None):
        super(SubdObject, self).__init__(coarse, scene, name, layer, visible)
        self._subd = None
        self._guids = []
        self._guid_coarse_vertex = {}
        self._guid_coarse_edge = {}
        self._guid_subd_edge = {}
        self._guid_subd = {}
        self._edge_strips = {}
        self._strip_division = {}
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self.settings.update(type(self).SETTINGS)
        if settings:
            self.settings.update(settings)

# --------------------------------------------------------------------------
# properties
# --------------------------------------------------------------------------
    @property
    def coarse(self):
        return self.item

    @coarse.setter
    def coarse(self, coarse):
        self.item = coarse
        self._guids = []
        self._guid_coarse_vertex = {}
        self._guid_coarse_edge = {}
        self._edge_strips = edge_strips(self.item)

    @property
    def subd(self):
        return self._subd

    @subd.setter
    def subd(self, subd):
        self._subd = subd
        self._guid_subd_edge = {}
        self._guid_subd = {}

    @property
    def guid_coarse_edge(self):
        """dict: Map between Rhino object GUIDs and skeleton vertex identifiers."""
        return self._guid_coarse_edge

    @guid_coarse_edge.setter
    def guid_coarse_edge(self, values):
        self._guid_coarse_edge = dict(values)

    @property
    def guid_subd_edge(self):
        """dict: Map between Rhino object GUIDs and skeleton vertex identifiers."""
        return self._guid_subd_edge

    @guid_subd_edge.setter
    def guid_subd_edge(self, values):
        self._guid_subd_edge = dict(values)


# --------------------------------------------------------------------------
# constructors
# --------------------------------------------------------------------------

    @classmethod
    def from_guid(cls, guid):
        rhinosurface = RhinoSurface.from_guid(guid)
        mesh = rhinosurface.to_compas()
        subdobject = cls(mesh)
        subdobject.coarse = mesh

        return subdobject

# --------------------------------------------------------------------------
# modification
# --------------------------------------------------------------------------

    def get_default_strip_subdvision(self):
        """get subdivision number for each strip by user input target length"""

        target_length = compas_rhino.rs.GetReal('target edge length?')
        for i, edges in self._edge_strips.items():
            edge0 = edges[0]
            n = int(round(self.item.edge_length(edge0[0], edge0[1]) / target_length))
            self._strip_division.update({i: n})

    def get_subd(self):
        subd = mesh_fast_copy(self.item)
        for i, edges in self._edge_strips.items():
            n = self._strip_division[i]
            subd = mesh_sbudivide_strip(subd, edges[0], n)

        self.subd = subd

    def _change_division(self, edge, n):
        """change subdivision for a strip"""
        for i, edges in self._edge_strips.items():
            if (edge[0], edge[1]) in edges or (edge[1], edge[0]) in edges:
                break

        self._strip_division.update({i: n})

    def change_strip_subd(self):
        """change subdivision for a strip, get input strip and division number from ui"""
        # guid = compas_rhino.select_lines('select the edge change subdivision')
        guid = rs.GetObjects(
            'select the edge change subdivision',
            preselect=False,
            select=True,
            group=False,
            filter=rs.filter.curve
            )
        if not guid:
            return

        edge = self.guid_coarse_edge[guid[0]]
        n = compas_rhino.rs.GetInteger('divide into?')

        self._change_division(edge, n)

        return guid

    def change_subd(self):
        while True:
            guid = self.change_strip_subd()
            if not guid:
                break

            self.clear_subd()
            self.get_subd()
            self.draw_subd()

# --------------------------------------------------------------------------
# visualize
# --------------------------------------------------------------------------

    def move(self):
        pass

    def modify(self):
        pass

    def select(self):
        pass

    def draw(self):
        pass

    def clear(self):
        pass

    def draw_coarse(self):
        guids = self.artist.draw_edges()
        self.guid_coarse_edge = zip(guids, list(self.item.edges()))
        self.artist.redraw()

    def draw_subd(self):

        artist = MeshArtist(self.subd)
        layer = self.settings['layer']
        color = self.settings['color.subd.edges']
        artist.layer = layer
        guids = artist.draw_edges(color=color)
        self.guid_subd_edge = zip(guids, list(self.subd.edges()))
        artist.redraw()

    def clear_subd(self):
        guid_subd_edge = list(self.guid_subd_edge.keys())
        delete_objects(guid_subd_edge, purge=True)
        self._guid_subd_edge = {}
