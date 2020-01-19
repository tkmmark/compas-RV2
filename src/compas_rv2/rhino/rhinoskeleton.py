from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.utilities import objects

from compas_rhino.helpers import mesh_draw_edges
from compas_rhino.helpers import mesh_draw_vertices
from compas_rhino.helpers import mesh_select_vertex
from compas_rhino.helpers import mesh_move_vertex
from compas_rhino.artists import MeshArtist

import Rhino
from Rhino.Geometry import Point3d
from Rhino.Geometry import Line
from System.Drawing.Color import FromArgb

import rhinoscriptsyntax as rs


__all__ = ["RhinoSkeleton"]


class RhinoSkeleton(object):

    def __init__(self, diagram):
        self.diagram = diagram

    def artist(self):
        return MeshArtist(self.diagram.to_diagram())

    def dynamic_draw_self(self):
        """ Update the skeleton leaf width and node width with dynamic draw. """
        self.dynamic_draw('both_width')
        mesh_draw_edges(self.diagram.to_diagram(), layer='skeleton_diagram_edges', clear_layer=True)

        self.dynamic_draw('node_width')
        self.draw_self()

    def dynamic_draw(self, flag):
        gp = Rhino.Input.Custom.GetPoint()
        if flag == 'node_width':
            gp.SetCommandPrompt('select a skeleton node vertex')
        else:
            gp.SetCommandPrompt('select a skeleton leaf vertex')
        gp.Get()
        sp = gp.Point()
        gp.SetCommandPrompt('confirm the diagram width')

        try:
            rs.PurgeLayer('skeleton_diagram_edges')
        except:  # noqa: E722
            pass

        def OnDynamicDraw(sender, e):
            cp = e.CurrentPoint
            dist = cp.DistanceTo(sp)
            self.diagram._update_width(dist, flag)
            self.diagram._update_mesh_vertices_pos()
            lines = self._get_edge_lines_in_rhino()

            for line in lines:
                e.Display.DrawLine(line, FromArgb(0, 0, 0), 2)

        gp.DynamicDraw += OnDynamicDraw

        gp.Get()
        ep = gp.Point()
        dist = ep.DistanceTo(sp)

        self.diagram._update_width(dist, flag)
        self.diagram._update_mesh_vertices_pos()

    def move_skeleton_vertex(self):
        """ Change the position of a skeleton vertex and update all the other vertices. """
        key = mesh_select_vertex(self.diagram)
        if self.diagram.vertex[key]['type'] == 'skeleton_node' or self.diagram.vertex[key]['type'] == 'skeleton_leaf':
            mesh_move_vertex(self.diagram, key)
            self.update_diagram()
        else:
            print('Not a skeleton vertex! Please select again:')
            pass

    def move_diagram_vertext(self):
        """ Change the position of the mesh vertcies.
        Notice that by this function, change of selected vertex won't affect others.
        This is different from the Skeleton.move_skeleton_vertex().
        """
        keys = mesh_select_vertex(self.diagram)
        mesh_move_vertex(self.diagram, keys)

    def update_diagram(self):
        self.diagram._update_mesh_vertices_pos()

    def _get_edge_lines_in_rhino(self):
        """ Get rhino object lines for dynamic darw. """
        sub_mesh = self.diagram.to_diagram()
        edge_lines = []
        for u, v in sub_mesh.edges():
            pts = sub_mesh.edge_coordinates(u, v)
            line = Line(Point3d(*pts[0]), Point3d(*pts[1]))
            edge_lines.append(line)

        return edge_lines

    def draw_self(self):
        """ Draw the skeleton mesh in Rhino.
        Below will be drawn:
            skeleton vertices
            skeleton branches
            low poly mesh vertices
            high poly mesh edges
        """
        skeleton_vertices = self.diagram.skeleton_vertices()[0] + self.diagram.skeleton_vertices()[1]
        skeleton_branches = self.diagram.skeleton_branches()
        boundary_vertices = list(set(range(0, self.diagram.number_of_vertices())) - set(skeleton_vertices))

        artist = self.artist()

        artist.layer = 'skeleton_vertices'
        artist.clear_layer()
        artist.draw_vertices(keys=skeleton_vertices, color=(255, 0, 0))

        artist.layer = 'skeleton_edges'
        artist.clear_layer()
        artist.draw_edges(keys=skeleton_branches, color=(0, 255, 0))

        artist.layer = 'skeleton_diagram_vertices'
        artist.clear_layer()
        artist.draw_vertices(keys=boundary_vertices, color=(0, 0, 0))

        artist.layer = 'skeleton_diagram_edges'
        artist.clear_layer()
        artist.draw_edges(color=(0, 0, 0))
        artist.redraw()

    def update_in_rhino(self):
        # this part should be embeded in UI

        while True:
            operation = rs.GetString('next')
            if operation == 'move_skeleton':
                self.move_skeleton_vertex()
                self.draw_self()
            elif operation == 'move_diagram':
                self.move_diagram_vertext()
                self.draw_self()
            elif operation == 'leaf_width':
                self.dynamic_draw('leaf_width')
                self.draw_self()
            elif operation == 'node_width':
                self.dynamic_draw('node_width')
                self.draw_self()

            elif operation == 'subdivide':
                self.diagram.subdivide(k=1)
                self.draw_self()
            elif operation == 'merge':
                self.diagram.merge(k=1)
                self.draw_self()

            elif operation == 'add_lines':
                try:
                    rs.PurgeLayer('skeleton_vertices')
                    rs.PurgeLayer('skeleton_diagram_vertices')
                    rs.PurgeLayer('skeleton_diagram_edges')
                except:  # noqa E722
                    pass

                line_ids = rs.GetObjects("select curves to add", filter=rs.filter.curve)
                lines = objects.get_line_coordinates(line_ids)
                rs.DeleteObjects(line_ids)
                self.diagram.add_skeleton_lines(lines)
                self.draw_self()

            elif operation == 'remove_lines':
                skeleton_branches = self.diagram.skeleton_branches()
                branch_names = []
                for branch in skeleton_branches:
                    branch_names.append('Mesh.edge.{0}-{1}'.format(branch[0], branch[1]))

                def custom_filter(rhino_object, geometry, component_index):
                    if rhino_object.Attributes.Name in branch_names:
                        return True
                    return False

                try:
                    rs.PurgeLayer('skeleton_vertices')
                    rs.PurgeLayer('skeleton_diagram_vertices')
                    rs.PurgeLayer('skeleton_diagram_edges')
                except:  # noqa E722
                    pass

                line_ids = rs.GetObjects('select a skeleton line to remove', custom_filter=custom_filter)

                remove_branches = []
                for line_id in line_ids:
                    name = rs.ObjectName(line_id)
                    branch = (int(name[-3]), int(name[-1]))
                    remove_branches.append(branch)

                self.diagram.remove_skeleton_lines(remove_branches)
                self.draw_self()

            elif operation == 'export':
                diagram = self.diagram.to_diagram()
                mesh_draw_edges(diagram, layer='form diagram')
                mesh_draw_vertices(diagram, color=(0, 0, 255), layer='form diagram')
            elif operation == 'stop':
                rs.PurgeLayer('skeleton_vertices')
                break
            else:
                break


if __name__ == '__main__':
    pass
