from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import Rhino
# from Rhino.Geometry import Point3d

import compas_rhino
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
# from compas.geometry import subtract_vectors
# from compas.geometry import add_vectors
# from compas.geometry import scale_vector

from compas_rhino.objects import BaseObject
# from compas_rhino.objects.modify import mesh_update_attributes
# from compas_rhino.objects.modify import mesh_update_vertex_attributes
# from compas_rhino.objects.modify import mesh_update_face_attributes
# from compas_rhino.objects.modify import mesh_update_edge_attributes
# from compas_rhino.objects.modify import mesh_move_vertex
# from compas_rhino.objects.modify import mesh_move_vertices
# from compas_rhino.objects.modify import mesh_move_face


__all__ = ["SkeletonObject"]


class SkeletonObject(BaseObject):
    """Scene object for Skeleton in Rhino."""

    SETTINGS = {
        'color.vertices': (255, 255, 255),
        'color.edges': (0, 0, 0),
        'color.faces': (0, 0, 0),
        'color.mesh': (0, 0, 0),
        'show.mesh': True,
        'show.vertices': True,
        'show.edges': True,
        'show.faces': False,
    }

    # modify = mesh_update_attributes
    # modify_vertices = mesh_update_vertex_attributes
    # modify_faces = mesh_update_face_attributes
    # modify_edges = mesh_update_edge_attributes

    def __init__(self, skeleton, scene=None, name=None, layer=None, visible=True, settings=None):
        super(SkeletonObject, self).__init__(skeleton, scene, name, layer, visible)
        self._guids = []
        self._guid_skeleton_vertex = {}
        self._guid_skeleton_edge = {}
        self._guid_mesh_vertex = {}
        self._guid_mesh_edge = {}
        self._guid_mesh_face = {}
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self.settings.update(type(self).SETTINGS)
        if settings:
            self.settings.update(settings)

    @property
    def skeleton(self):
        return self.item

    @skeleton.setter
    def skeleton(self, skeleton):
        self.item = skeleton
        self._guids = []
        self._guid_skeleton_vertex = {}
        self._guid_skeleton_edge = {}
        self._guid_mesh_vertex = {}
        self._guid_mesh_edge = {}
        self._guid_mesh_face = {}

    # def __getstate__(self):
    #     pass

    # def __setstate__(self, state):
    #     pass

    @property
    def anchor(self):
        """The vertex of the mesh that is anchored to the location of the object."""
        return self._anchor

    @anchor.setter
    def anchor(self, vertex):
        if self.skeleton.has_vertex(vertex):
            self._anchor = vertex

    @property
    def location(self):
        """:class:`compas.geometry.Point`:
        The location of the object.
        Default is the origin of the world coordinate system.
        The object transformation is applied relative to this location.

        Setting this location will make a copy of the provided point object.
        Moving the original point will thus not affect the object's location.
        """
        if not self._location:
            self._location = Point(0, 0, 0)
        return self._location

    @location.setter
    def location(self, location):
        self._location = Point(*location)

    @property
    def scale(self):
        """float:
        A uniform scaling factor for the object in the scene.
        The scale is applied relative to the location of the object in the scene.
        """
        if not self._scale:
            self._scale = 1.0
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def rotation(self):
        """list of float:
        The rotation angles around the 3 axis of the coordinate system
        with the origin placed at the location of the object in the scene.
        """
        if not self._rotation:
            self._rotation = [0, 0, 0]
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def vertex_xyz(self):
        """dict : The view coordinates of the mesh object."""
        origin = Point(0, 0, 0)
        if self.anchor is not None:
            xyz = self.skeleton.vertex_attributes(self.anchor, 'xyz')
            point = Point(* xyz)
            T1 = Translation.from_vector(origin - point)
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T2 = Translation.from_vector(self.location)
            X = T2 * R * S * T1
        else:
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T = Translation.from_vector(self.location)
            X = T * R * S
        skeleton = self.skeleton.transformed(X)
        vertex_xyz = {vertex: skeleton.vertex_attributes(vertex, 'xyz') for vertex in skeleton.vertices()}
        return vertex_xyz

    @property
    def guid_skeleton_vertex(self):
        """dict: Map between Rhino object GUIDs and skeleton vertex identifiers."""
        return self._guid_skeleton_vertex

    @guid_skeleton_vertex.setter
    def guid_skeleton_vertex(self, values):
        self._guid_skeleton_vertex = dict(values)

    @property
    def guid_skeleton_edge(self):
        """dict: Map between Rhino object GUIDs and skeleton edge identifiers."""
        return self._guid_skeleton_edge

    @guid_skeleton_edge.setter
    def guid_skeleton_edge(self, values):
        self._guid_skeleton_edge = dict(values)

    @property
    def guid_mesh_vertex(self):
        """dict: Map between Rhino object GUIDs and mesh vertex identifiers."""
        return self._guid_mesh_vertex

    @guid_mesh_vertex.setter
    def guid_mesh_vertex(self, values):
        self._guid_mesh_vertex = dict(values)

    @property
    def guid_mesh_edge(self):
        """dict: Map between Rhino object GUIDs and mesh edge identifiers."""
        return self._guid_mesh_edge

    @guid_mesh_edge.setter
    def guid_mesh_edge(self, values):
        self._guid_mesh_edge = dict(values)

    @property
    def guid_mesh_face(self):
        """dict: Map between Rhino object GUIDs and mesh face identifiers."""
        return self._guid_mesh_face

    @guid_mesh_face.setter
    def guid_mesh_face(self, values):
        self._guid_mesh_face = dict(values)

    @property
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        guids = self._guids
        guids += list(self.guid_skeleton_vertex)
        guids += list(self.guid_skeleton_edge)
        guids += list(self.guid_mesh_vertex)
        guids += list(self.guid_mesh_edge)
        guids += list(self.guid_mesh_face)
        return guids

    def clear(self):
        """Clear all Rhino objects associated with this object.
        """
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_skeleton_vertex = {}
        self._guid_skeleton_edge = {}
        self._guid_mesh_vertex = {}
        self._guid_mesh_edge = {}
        self._guid_mesh_face = {}

    def draw(self):
        """Draw the object representing the mesh.
        """
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        # conditional drawing based on settings
        # similar to mesh, network, diagram ...
