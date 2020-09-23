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
from compas.geometry import Vector
from compas.geometry import dot_vectors
from compas.geometry import add_vectors
from compas_rhino.objects import mesh_move_vertex
from compas_rhino import delete_objects
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
try:
    import Rhino.Input.Custom
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line
    from System.Drawing.Color import FromArgb
except ImportError:
    pass


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
        self._guid_subd = {}
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
        self._guid_subd = {}

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
    def guid_subd(self):
        """dict: Map between Rhino object GUIDs and mesh face identifiers."""
        return self._guid_subd

    @guid_subd.setter
    def guid_subd(self, values):
        self._guid_subd = dict(values)

    @property
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        guids = self._guids
        guids += list(self.guid_skeleton_vertex)
        guids += list(self.guid_skeleton_edge)
        guids += list(self.guid_mesh_vertex)
        guids += list(self.guid_mesh_edge)
        guids += list(self.guid_mesh_face)
        guids += list(self.guid_subd)
        return guids

    # ==============================================================================
    # Visualize
    # ==============================================================================

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
        self._guid_subd = {}

    def clear_skeleton(self):
        pass

    def clear_corse_mesh_vertices(self):
        pass

    def clear_subd(self):
        guid_subd = list(self.guid_subd.keys())
        compas_rhino.delete_objects(guid_subd, purge=True)
        self._guid_subd = {}

    def draw(self):
        """Draw the object representing the mesh.
        """
        self.clear()
        if not self.visible:
            return
        # self.artist.vertex_xyz = self.vertex_xyz
        # self.artist.subd_vertex_xyz = self.subd_vertex_xyz

        self.draw_skeleton()
        self.draw_subd()

        # conditional drawing based on settings
        # similar to mesh, network, diagram ...

    def draw_skeleton(self):
        skeleton_vertices = list(self.skeleton.skeleton_vertices[0] + self.skeleton.skeleton_vertices[1])
        guids_vertices = self.artist.draw_skeleton_vertices(skeleton_vertices)
        self.guid_skeleton_vertex = zip(guids_vertices, skeleton_vertices)

        skeleton_edges = list(self.skeleton.skeleton_branches)
        guids_edges = self.artist.draw_skeleton_edges(skeleton_edges)
        self.guid_skeleton_edge = zip(guids_edges, skeleton_edges)

    def draw_coarse_mesh_vertices(self):
        pass

    def draw_subd(self):
        self.artist.subd = self.skeleton.to_mesh()
        guids = list(self.artist.draw_subd())
        self.guid_subd = zip(guids, [None])

    def move(self):
        pass

    def modify(self):
        pass

    def select(self):
        pass

    def dynamic_draw_widths(self):
        """Dynamic draw leaf width, node width, leaf extend and update the mesh in rhino.

        Examples
        --------
        >>> lines = [
        >>> ([0.0, 0.0, 0.0], [0.0, 10.0, 0.0]),
        >>> ([0.0, 0.0, 0.0], [-8.6, -5.0, 0.0]),
        >>> ([0.0, 0.0, 0.0], [8.6, -5.0, 0.0])
        >>> ]
        >>> skeleton = Skeleton.from_skeleton_lines(lines)
        >>> skeletonobjcet = SkeletonObject(skeleton)
        >>> skeletonobjcet.dynamic_draw_widths()

        """
        if self.skeleton.skeleton_vertices[1]:
            result = self.dynamic_draw_width('leaf_width')
            if result == Rhino.Commands.Result.Cancel:
                return False

        if self.skeleton.skeleton_vertices[0]:
            result = self.dynamic_draw_width('node_width')
            if result == Rhino.Commands.Result.Cancel:
                return False

        if self.skeleton.skeleton_vertices[1]:
            result = self.dynamic_draw_width('leaf_extend')
            if result == Rhino.Commands.Result.Cancel:
                return False

        return True

    def dynamic_draw_width(self, param):
        """Dynamic draw a width value, and update the mesh in rhino.

        Parameters
        -----------
        param: str
            'node_width', 'leaf_width', 'leaf_extend'

        Examples
        --------
        >>> lines = [
        >>> ([0.0, 0.0, 0.0], [0.0, 10.0, 0.0]),
        >>> ([0.0, 0.0, 0.0], [-8.6, -5.0, 0.0]),
        >>> ([0.0, 0.0, 0.0], [8.6, -5.0, 0.0])
        >>> ]
        >>> skeleton = Skeleton.from_skeleton_lines(lines)
        >>> skeletonobjcet = SkeletonObject(skeleton)
        >>> skeletonobjcet.dynamic_draw_width('node_width')
        """

        # get start point
        gp = Rhino.Input.Custom.GetPoint()
        if param == 'node_width':
            node_vertex = self.skeleton.skeleton_vertices[0][0]
            sp = Point3d(*(self.skeleton.vertex_coordinates(node_vertex)))
            gp.SetCommandPrompt('select the node vertex')
        else:
            leaf_vertex = self.skeleton.skeleton_vertices[1][0]
            sp = Point3d(*(self.skeleton.vertex_coordinates(leaf_vertex)))
            gp.SetCommandPrompt('select the leaf vertex')

        gp.SetBasePoint(sp, False)
        gp.ConstrainDistanceFromBasePoint(0.01)
        gp.Get()
        print(gp.CommandResult())
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return gp.CommandResult()

        sp = gp.Point()

        gp.SetCommandPrompt('confirm the distance')
        self.clear_subd()

        # get current point
        def OnDynamicDraw(sender, e):
            cp = e.CurrentPoint
            e.Display.DrawDottedLine(sp, cp, FromArgb(0, 0, 0))

            mp = Point3d.Add(sp, cp)
            mp = Point3d.Divide(mp, 2)
            dist = cp.DistanceTo(sp)
            e.Display.Draw2dText(str(dist), FromArgb(0, 0, 0), mp, False, 20)

            if param == 'leaf_extend':
                direction = _get_leaf_extend_direction(cp)
                dist *= direction

            self.skeleton._update_width(dist, param)
            self.skeleton.update_mesh_vertices_pos()
            lines = _get_edge_lines_in_rhino()

            for line in lines:
                e.Display.DrawLine(line, FromArgb(0, 0, 0), 2)

        def _get_constrain(param):
            u = leaf_vertex
            vec_along_edge = self.skeleton._get_vec_along_branch(u)

            if param == 'leaf_width':
                vec_offset = vec_along_edge.cross(Vector.Zaxis())
                vec_rhino = Rhino.Geometry.Vector3d(vec_offset[0], vec_offset[1], vec_offset[2])

            if param == 'leaf_extend':
                vec_rhino = Rhino.Geometry.Vector3d(vec_along_edge[0], vec_along_edge[1], vec_along_edge[2])

            pt_leaf = Point3d(*(self.skeleton.vertex_coordinates(u)))
            line = Line(pt_leaf, vec_rhino)
            return line

        def _get_leaf_extend_direction(cp):
            u = leaf_vertex
            vec_along_edge = self.skeleton._get_vec_along_branch(u)
            vec_sp_np = Vector.from_start_end(sp, cp)
            dot_vec = dot_vectors(vec_along_edge, vec_sp_np)

            if dot_vec == 0:
                return 0

            return dot_vec / abs(dot_vec)

        def _get_edge_lines_in_rhino():
            sub_mesh = self.skeleton.to_mesh()
            edge_lines = []
            for u, v in sub_mesh.edges():
                pts = sub_mesh.edge_coordinates(u, v)
                line = Line(Point3d(*pts[0]), Point3d(*pts[1]))
                edge_lines.append(line)

            return edge_lines

        if param == 'leaf_width' or param == 'leaf_extend':
            gp.Constrain(_get_constrain(param))
        gp.DynamicDraw += OnDynamicDraw

        # get end point
        gp.Get()
        ep = gp.Point()

        dist = ep.DistanceTo(sp)

        if param == 'leaf_extend':
            direction = _get_leaf_extend_direction(ep)
            dist *= direction

        self.skeleton._update_width(dist, param)
        self.skeleton.update_mesh_vertices_pos()

        self.draw_subd()
        return gp.CommandResult()
