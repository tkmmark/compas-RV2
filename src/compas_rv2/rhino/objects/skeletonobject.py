from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Vector

import compas_rhino
from compas_rhino.selectors import mesh_select_vertex
from compas_rhino.modifiers import mesh_move_vertex
from compas_rhino.artists import MeshArtist
from compas_rhino import draw_points
from compas_rhino import draw_lines

import Rhino
from Rhino.Geometry import Point3d
from Rhino.Geometry import Line
from System.Drawing.Color import FromArgb

import rhinoscriptsyntax as rs


__all__ = ["SkeletonObject"]


class SkeletonObject(object):

    def __init__(self, skeleton):
        self.datastructure = skeleton
        # self.draw_skeleton_branches()

    def add_lines(self):
        try:
            rs.PurgeLayer('RV2::Skeleton::skeleton_vertices')
            rs.PurgeLayer('RV2::Skeleton::diagram_vertices')
            rs.PurgeLayer('RV2::Skeleton::diagram_edges')
        except:  # noqa E722
            pass

        guids = compas_rhino.select_lines()
        if not guids:
            return
        lines = compas_rhino.get_line_coordinates(guids)
        rs.DeleteObjects(guids)
        self.datastructure.add_skeleton_lines(lines)

    def remove_lines(self):
        skeleton_branches = self.datastructure.skeleton_branches()
        branch_names = []
        for branch in skeleton_branches:
            branch_names.append('Mesh.edge.{0}-{1}'.format(branch[0], branch[1]))

        def custom_filter(rhino_object, geometry, component_index):
            if rhino_object.Attributes.Name in branch_names:
                return True
            return False

        try:
            rs.PurgeLayer('RV2::Skeleton::skeleton_vertices')
            rs.PurgeLayer('RV2::Skeleton::diagram_vertices')
            rs.PurgeLayer('RV2::Skeleton::diagram_edges')
        except:  # noqa E722
            pass

        line_ids = rs.GetObjects('select skeleton lines to remove', custom_filter=custom_filter)

        remove_branches = []
        for line_id in line_ids:
            name = rs.ObjectName(line_id)
            branch = (int(name[-3]), int(name[-1]))
            remove_branches.append(branch)

        self.datastructure.remove_skeleton_lines(remove_branches)

    def dynamic_draw_self(self):
        """ Update the skeleton leaf width and node width with dynamic draw. """
        if self.datastructure.skeleton_vertices()[1] != []:
            self.dynamic_draw('both_width')
            artist = MeshArtist(self.datastructure.to_mesh())
            artist.layer = 'RV2::Skeleton::diagram_edges'
            artist.clear_layer()
            artist.draw_edges()
            artist.redraw()

        self.dynamic_draw('node_width')
        self.draw_self()

    def dynamic_draw(self, flag):

        gp = Rhino.Input.Custom.GetPoint()
        if flag == 'node_width':
            node_vertex = self.datastructure.skeleton_vertices()[0][0]
            sp = Point3d(*(self.datastructure.vertex_coordinates(node_vertex)))
            gp.SetCommandPrompt('select the node vertex')
        else:
            leaf_vertex = self.datastructure.skeleton_vertices()[1][0]
            sp = Point3d(*(self.datastructure.vertex_coordinates(leaf_vertex)))
            gp.SetCommandPrompt('select the leaf vertex')

        gp.SetBasePoint(sp, False)
        gp.ConstrainDistanceFromBasePoint(0.1)
        gp.Get()
        sp = gp.Point()
        gp.SetCommandPrompt('confirm the diagram width')

        try:
            rs.PurgeLayer('RV2::Skeleton::diagram_edges')
        except:  # noqa: E722
            pass

        def OnDynamicDraw(sender, e):
            cp = e.CurrentPoint
            e.Display.DrawDottedLine(sp, cp, FromArgb(0, 0, 0))

            mp = Point3d.Add(sp, cp)
            mp = Point3d.Divide(mp, 2)
            dist = cp.DistanceTo(sp)
            e.Display.Draw2dText(str(dist), FromArgb(0, 0, 0), mp, False, 20)

            self.datastructure._update_width(dist, flag)
            self.datastructure.update_mesh_vertices_pos()
            lines = self._get_edge_lines_in_rhino()

            for line in lines:
                e.Display.DrawLine(line, FromArgb(0, 0, 0), 2)

        if flag != 'node_width':
            u = leaf_vertex
            v = None
            for key in self.datastructure.halfedge[u]:
                if self.datastructure.vertex[key]['type'] == 'skeleton_node':
                    v = key

            vec_along_edge = Vector(*(self.datastructure.edge_vector(v, u)))
            vec_offset = vec_along_edge.cross(Vector.Zaxis())
            vec_rhino = Rhino.Geometry.Vector3d(vec_offset[0], vec_offset[1], vec_offset[2])

            pt_leaf = Point3d(*(self.datastructure.vertex_coordinates(u)))
            line = Line(pt_leaf, vec_rhino)
            gp.Constrain(line)

        gp.DynamicDraw += OnDynamicDraw

        gp.Get()
        ep = gp.Point()
        dist = ep.DistanceTo(sp)

        self.datastructure._update_width(dist, flag)
        self.datastructure.update_mesh_vertices_pos()

    def move_skeleton_vertex(self):
        """ Change the position of a skeleton vertex and update all the other vertices. """
        key = mesh_select_vertex(self.datastructure)
        if self.datastructure.vertex[key]['type'] == 'skeleton_node' or self.datastructure.vertex[key]['type'] == 'skeleton_leaf':
            mesh_move_vertex(self.datastructure, key)
            self.update_diagram()
        else:
            print('Not a skeleton vertex! Please select again:')
            pass

    def move_diagram_vertex(self):
        """ Change the position of the mesh vertcies.
        Notice that by this function, change of selected vertex won't affect others.
        This is different from the Skeleton.move_skeleton_vertex().
        """
        keys = mesh_select_vertex(self.datastructure)
        mesh_move_vertex(self.datastructure, keys)

    def update_diagram(self):
        self.datastructure.update_mesh_vertices_pos()

    def _get_edge_lines_in_rhino(self):
        """ Get rhino object lines for dynamic darw. """
        sub_mesh = self.datastructure.to_mesh()
        edge_lines = []
        for u, v in sub_mesh.edges():
            pts = sub_mesh.edge_coordinates(u, v)
            line = Line(Point3d(*pts[0]), Point3d(*pts[1]))
            edge_lines.append(line)

        return edge_lines

    def draw_skeleton_branches(self):
        skeleton_vertices = self.datastructure.skeleton_vertices()[0] + self.datastructure.skeleton_vertices()[1]
        skeleton_branches = self.datastructure.skeleton_branches()

        pts = []
        for key in skeleton_vertices:
            pts.append({'pos': self.datastructure.vertex_coordinates(key), 'color': (255, 0, 0)})
        draw_points(pts, layer='RV2::Skeleton::skeleton_vertices', clear=True, redraw=False)

        lines = []
        for u, v in skeleton_branches:
            lines.append({
                'start': self.datastructure.vertex_coordinates(u),
                'end': self.datastructure.vertex_coordinates(v),
                'color': (0, 255, 0)
            })
        draw_lines(lines, layer='RV2::Skeleton::skeleton_edges', clear=True, redraw=True)

    def draw_self(self):
        """ Draw the skeleton mesh in Rhino.
        Below will be drawn:
            skeleton vertices
            skeleton branches
            low poly mesh vertices
            high poly mesh edges
        """
        skeleton_vertices = self.datastructure.skeleton_vertices()[0] + self.datastructure.skeleton_vertices()[1]
        skeleton_branches = self.datastructure.skeleton_branches()
        boundary_vertices = list(set(range(0, self.datastructure.number_of_vertices())) - set(skeleton_vertices))

        artist = MeshArtist(self.datastructure)

        artist.layer = 'RV2::Skeleton::skeleton_vertices'
        artist.clear_layer()
        artist.draw_vertices(keys=skeleton_vertices, color=(255, 0, 0))

        if skeleton_branches != []:
            artist.layer = 'RV2::Skeleton::skeleton_edges'
            artist.clear_layer()
            artist.draw_edges(keys=skeleton_branches, color=(0, 255, 0))

        artist = MeshArtist(self.datastructure.to_mesh())

        artist.layer = 'RV2::Skeleton::diagram_vertices'
        artist.clear_layer()
        artist.draw_vertices(keys=boundary_vertices, color=(0, 0, 0))

        artist.layer = 'RV2::Skeleton::diagram_edges'
        artist.clear_layer()
        artist.draw_edges(color=(0, 0, 0))
        artist.redraw()

    def draw_rhino_mesh(self):
        artist = MeshArtist(self.datastructure.to_mesh())
        artist.layer = 'RV2::Skeleton::mesh'
        artist.draw_mesh()
        artist.redraw()

    def update(self):
        # this part should be embeded in UI

        while True:
            operation = rs.GetString('next')
            if operation == 'move_skeleton':
                self.move_skeleton_vertex()
            elif operation == 'move_diagram':
                self.move_diagram_vertex()
            elif operation == 'leaf_width':
                if self.datastructure.skeleton_vertices()[1] != []:
                    self.dynamic_draw('leaf_width')
                else:
                    print('this skeleton doesn\'t have any leaf!')
            elif operation == 'node_width':
                self.dynamic_draw('node_width')
            elif operation == 'subdivide':
                self.datastructure.subdivide(k=1)
            elif operation == 'merge':
                self.datastructure.merge(k=1)
            elif operation == 'add_lines':
                self.add_lines()
            elif operation == 'remove_lines':
                self.remove_lines()

            # elif operation == 'export':
            #     rs.PurgeLayer('RV2::Skeleton::skeleton_vertices')
            #     rs.PurgeLayer('RV2::Skeleton::diagram_vertices')
            #     diagram = self.datastructure.to_mesh()
            #     mesh_draw_edges(diagram, layer='form diagram')
            #     mesh_draw_vertices(diagram, color=(0, 0, 255), layer='form diagram')
            elif operation == 'stop':
                self.draw_self()
                break
            else:
                self.draw_self()
                break

            self.draw_self()

    def draw(self):
        # PLACEHOLDER
        pass

if __name__ == '__main__':
    pass
