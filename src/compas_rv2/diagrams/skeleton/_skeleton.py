from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas.datastructures import mesh_subdivide_catmullclark
from compas.datastructures import Network
from compas.datastructures.network import duality

from compas.geometry import centroid_points
from compas.geometry import Vector
from compas.geometry import add_vectors

from compas_rhino.utilities import objects

from compas_rhino.helpers import network_draw
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
import copy


class Skeleton(Mesh):
    """ class Skeleton is a low poly mesh.
    It stores a few attributes representing a 'skeleton' which functions as the central spine of the mesh.
    Editing skeleton vertices and branches can affect the entire mesh.
    It can display and generate high poly mesh as diagrams for compas_tna.
    """

    def __init__(self):
        super(Skeleton, self).__init__()
        self.attributes.update({
            'leaf_width': 0,
            'node_width': 0,
            'sub_level': 1,
        })
        self.default_vertex_attributes.update({'type': None})
        self.default_edge_attributes.update({'type': None})

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_skeleton_lines(cls, lines=[]):
        """ Instantiate a Network with lines, generate the skeleton data structure with Network. """
        skeleton = cls()

        network = Network.from_lines(lines)
        network_draw(network, layer='skeleton_edges', clear_layer=False, vertexcolor=(255, 0, 0), edgecolor=(0, 255, 0))

        skeleton.mesh_from_network(network)

        return skeleton

    def add_skeleton_lines(self, lines=[]):
        """ Update skeleton mesh structure from a new network which is created with the currrent skeleton lines and added lines.
        The leaf_width, node_width, sub_level will remain the same.
        """
        current_lines = []
        for u, v, attr in self.edges(True):
            if attr['type'] == 'skeleton_branch':
                line = [self.vertex_coordinates(u), self.vertex_coordinates(v)]
                current_lines.append(line)

        current_lines += lines
        network = Network.from_lines(current_lines)

        self.clear()
        self.mesh_from_network(network)
        self._update_mesh_vertices_pos()

    def remove_skeleton_lines(self, line_keys=[]):
        """ Update skeleton mesh structure from a new network which is created with the currrent skeleton lines subtract added lines.
        The leaf_width, node_width, sub_level will remain the same.
        """
        new_line_keys = list(set(self.skeleton_branches()) - set(line_keys))

        new_lines = []
        for u, v in new_line_keys:
            line = self.edge_coordinates(u, v)
            new_lines.append(line)

        network = Network.from_lines(new_lines)

        self.clear()
        self.mesh_from_network(network)
        self._update_mesh_vertices_pos()

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def mesh_from_network(self, network):
        """ Store network vertices and skeleton node vertices and leaf vertices.
        Stire network edges and skeleton branches.
        For each network halfedge, add one face to the Skeleton.
        """
        self._add_skeleton_vertices(network)
        self._add_skeleton_branches(network)
        network = self._add_boundary_vertices(network)
        self._add_mesh_faces(network)

    def _add_skeleton_vertices(self, network):
        duality._sort_neighbors(network, True)

        for key in network.vertices():
            if network.is_vertex_leaf(key):
                network.vertex[key].update({'type': 'skeleton_leaf'})
            else:
                network.vertex[key].update({'type': 'skeleton_node'})

            self.add_vertex(key)
            self.vertex[key].update(network.vertex[key])

    def _add_skeleton_branches(self, network):
        self.halfedge = copy.deepcopy(network.halfedge)
        self.update_default_edge_attributes({'type': None})
        for u, v in network.edges():
            self.edgedata[(u, v)].update({'type': 'skeleton_branch'})

    def _add_boundary_vertices(self, network):
        """ Assgin two new keys to each network halfedge so a face can be added to skeleton.

        for each skeleton node vertex, iterate all halfedges which start form it.
        assign a new vertex key to each of the halfedge,
        store it as the 'sp' for this halfedge[u][v],
        store it as the 'ep' for the adjacent halfedge[prvs, u].

        for each skeleton leaf vertex, assign two new vertex keys.
        store it as 'sp' for haledge[u][v] whitch starts from this leaf vertex,
        store another one as 'ep' for [v][u] which ends to it.

        after all iterations, each halfedge will have a 'sp' and an 'ep'. A face = [u, v, 'ep', 'sp'] could be added to skeleton.
        """
        def get_boundary_vertex_keys(network, u, v, sp=None, ep=None):
            attr = network.halfedge[u][v]
            if attr is None:
                attr = {}
            if sp is not None:
                attr['sp'] = sp
            if ep is not None:
                attr['ep'] = ep

            network.halfedge[u][v] = attr

        current_key = network.number_of_vertices()
        node_vertices, leaf_vertices = self.skeleton_vertices()

        for u in node_vertices:
            for v in network.halfedge[u]:

                vertex_prvs = self._find_previous_vertex(u, v)
                get_boundary_vertex_keys(network, u, v, sp=current_key)
                get_boundary_vertex_keys(network, vertex_prvs, u, ep=current_key)

                self.add_vertex(current_key)

                current_key += 1

        for u in leaf_vertices:
            v = network.halfedge[u].items()[0][0]

            get_boundary_vertex_keys(network, u, v, sp=current_key)
            get_boundary_vertex_keys(network, v, u, ep=current_key+1)

            self.add_vertex(current_key)
            self.add_vertex(current_key+1)

            current_key += 2

        return network

    def _add_mesh_faces(self, network):
        for u in network.halfedge:
            for v in network.halfedge[u]:
                self.add_face([
                    u, v,
                    network.halfedge[u][v]['ep'],
                    network.halfedge[u][v]['sp']
                ])

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    def dynamic_draw_self(self):
        """ Update the skeleton leaf width and node width with dynamic draw. """
        self.dynamic_draw('both_width')
        mesh_draw_edges(self._subdivide(k=self.attributes['sub_level']), layer='skeleton_diagram_edges', clear_layer=True)

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
            self._update_width(dist, flag)
            self._update_mesh_vertices_pos()
            lines = self._get_edge_lines_in_rhino()

            for line in lines:
                e.Display.DrawLine(line, FromArgb(0, 0, 0), 2)

        gp.DynamicDraw += OnDynamicDraw

        gp.Get()
        ep = gp.Point()
        dist = ep.DistanceTo(sp)

        self._update_width(dist, flag)
        self._update_mesh_vertices_pos()

    def move_skeleton_vertex(self):
        """ Change the position of a skeleton vertex and update all the other vertices. """
        key = mesh_select_vertex(self)
        if self.vertex[key]['type'] == 'skeleton_node' or self.vertex[key]['type'] == 'skeleton_leaf':
            mesh_move_vertex(self, key)
            self._update_mesh_vertices_pos()
        else:
            print('Not a skeleton vertex! Please select again:')
            pass

    def move_diagram_vertext(self):
        """ Change the position of the mesh vertcies.
        Notice that by this function, change of selected vertex won't affect others.
        This is different from the Skeleton.move_skeleton_vertex().
        """
        keys = mesh_select_vertex(self)
        mesh_move_vertex(self, keys)

    def _update_width(self, dist, flag):
        if flag == 'both_width':
            self.attributes['leaf_width'] = dist
            self.attributes['node_width'] = dist
        elif flag == 'leaf_width':
            self.attributes['leaf_width'] = dist
        else:
            self.attributes['node_width'] = dist

    def _update_mesh_vertices_pos(self):
        """
        There is a parent-children relationship between skeleton vertices and boundary vertices.
        This structure is stored in the face when the faces are created.
        When there is change of skeleton vertex position or the mesh width, the boundary vertices can be traced to be updated.
        """
        def update_node_boundary(u, v):
            fkey = self.halfedge[u][v]
            key = self.face[fkey][3]
            pt = self._get_node_boundary_vertex_pos(u, v)

            self.vertex[key].update({'x': pt[0], 'y': pt[1], 'z': pt[2]})

        def update_leaf_boundary(u, v):
            fkey1 = self.halfedge[u][v]
            fkey2 = self.halfedge[v][u]
            key1 = self.face[fkey1][3]
            key2 = self.face[fkey2][2]

            pt1, pt2 = self._get_leaf_boundary_vertex_pos(u, v)

            self.vertex[key1].update({'x': pt1[0], 'y': pt1[1], 'z': pt1[2]})
            self.vertex[key2].update({'x': pt2[0], 'y': pt2[1], 'z': pt2[2]})

        skeleton_branches = self.skeleton_branches()
        for u, v in skeleton_branches:
            if self.vertex[u]['type'] == 'skeleton_node':
                update_node_boundary(u, v)
            else:
                update_leaf_boundary(u, v)
            if self.vertex[v]['type'] == 'skeleton_node':
                update_node_boundary(v, u)
            else:
                update_leaf_boundary(v, u)

    def _get_node_boundary_vertex_pos(self, u, v):
        """ Find the xyz coordinates for a boundary vertex around a skeleton node.
        for each halfege[u][v] starting from a node vertex[u],
        the position of this boundary vertex is decided by the centroid of the triangle [prvs][u][v], and the node width.
        """
        vertex_prvs = self._find_previous_vertex(u, v)
        vec1 = Vector(*self.edge_vector(u, v))
        vec2 = Vector(*self.edge_vector(vertex_prvs, u))
        normal = vec1.cross(vec2)

        # if the two adjacent edges are parallel, the crossproduct length will be zero or nearly zero(tollerance).
        # then use world z instead.
        if normal.length < 0.001:
            vec_offset = Vector.Zaxis().cross(vec1)
        else:
            pt_face_center = centroid_points([
                self.vertex_coordinates(vertex_prvs),
                self.vertex_coordinates(u),
                self.vertex_coordinates(v)
                ])
            vec_offset = Vector.from_start_end(self.vertex_coordinates(u), pt_face_center)

            # if the vertex is at a convex corner, the offset direction should be flipped.
            vec_offset.scale(normal[2] * -1)

        vec_offset.unitize()
        vec_offset.scale(self.attributes['node_width'])
        pt_node = add_vectors(self.vertex_coordinates(u), vec_offset)

        return pt_node

    def _get_leaf_boundary_vertex_pos(self, u, v):
        """ Find the xyz coordinates for a pair of boundary vertices around a skeleton leaf.
        For each pair of halfedge that starts & ends at a skeleton leaf vertex,
        the positions of a pair of boundary vertices are decided by the leaf vertex, the edge vector and the leaf width.
        """
        vec_along_edge = Vector(*self.edge_vector(v, u))
        vec_offset = vec_along_edge.cross(Vector.Zaxis())
        if vec_offset.length < 0.001:
            raise Exception('skeleton line shouldn\'t be perpendicular to the ground')

        vec_offset.unitize()
        vec_offset.scale(self.attributes['leaf_width'])

        pt_leaf = self.vertex_coordinates(u)
        pt_leaf_right = add_vectors(pt_leaf, vec_offset)
        pt_leaf_left = add_vectors(pt_leaf, vec_offset.scaled(-1))

        return pt_leaf_right, pt_leaf_left

    def _find_previous_vertex(self, u, v):
        """ Find the previous vertex of a halfedge[u][v] through sorted nbrs. """
        nbrs = self.vertex[u]['sorted_neighbors']
        prvs = nbrs[(nbrs.index(v) + 1) % len(nbrs)]
        return prvs

    def skeleton_vertices(self):
        skeleton_nodes = []
        skeleton_leaves = []

        for key in self.vertex:
            if self.vertex[key]['type'] == 'skeleton_node':
                skeleton_nodes.append(key)
            elif self.vertex[key]['type'] == 'skeleton_leaf':
                skeleton_leaves.append(key)

        return skeleton_nodes, skeleton_leaves

    def skeleton_branches(self):
        skeleton_branches = []
        for u, v, attr in self.edges(True):
            if attr['type'] == 'skeleton_branch':
                skeleton_branches.append((u, v))

        return skeleton_branches

    # --------------------------------------------------------------------------
    # visualization
    # exporting digrams
    # --------------------------------------------------------------------------

    def _subdivide(self, k=1):
        corners = []
        for key in self.vertices():
            if self.vertex_degree(key) == 2:
                corners.append(key)

        return mesh_subdivide_catmullclark(self, k, fixed=corners)

    def _get_edge_lines_in_rhino(self):
        """ Get rhino object lines for dynamic darw. """
        sub_mesh = self._subdivide(k=self.attributes['sub_level'])
        edge_lines = []
        for u, v in sub_mesh.edges():
            pts = sub_mesh.edge_coordinates(u, v)
            line = Line(Point3d(*pts[0]), Point3d(*pts[1]))
            edge_lines.append(line)

        return edge_lines

    def subdivide(self, k=1):
        """ Increase & decrease subdivision level for displaying & exporting high poly mesh. """
        self.attributes['sub_level'] += k

    def merge(self, k=1):
        """ Increase & decrease subdivision level for displaying & exporting high poly mesh. """
        if self.attributes['sub_level'] > 1:
            self.attributes['sub_level'] -= k

    def draw_self(self):
        """ Draw the skeleton mesh in Rhino.
        Below will be drawn:
            skeleton vertices
            skeleton branches
            low poly mesh vertices
            high poly mesh edges
        """
        skeleton_vertices = self.skeleton_vertices()[0] + self.skeleton_vertices()[1]
        skeleton_branches = self.skeleton_branches()
        boundary_vertices = list(set(range(0, self.number_of_vertices())) - set(skeleton_vertices))

        artist = MeshArtist(self)
        artist.layer = 'skeleton_vertices'
        artist.clear_layer()
        artist.draw_vertices(keys=skeleton_vertices, color=(255, 0, 0))

        artist.layer = 'skeleton_edges'
        artist.clear_layer()
        artist.draw_edges(keys=skeleton_branches, color=(0, 255, 0))

        artist.layer = 'skeleton_diagram_vertices'
        artist.clear_layer()
        artist.draw_vertices(keys=boundary_vertices, color=(0, 0, 0))

        artist = MeshArtist(self._subdivide(k=self.attributes['sub_level']))
        artist.layer = 'skeleton_diagram_edges'
        artist.clear_layer()
        artist.draw_edges(color=(0, 0, 0))
        artist.redraw()

    def to_diagram(self):
        """ Diagram mesh(high poly) is a mesh without any additional attr or functions from class Skeleton.
        It cannot be edited again once exported as diagram for further analysis.
        """
        digram_mesh = Mesh()
        highpoly_mesh = self._subdivide(self.attributes['sub_level'])

        for key, attr in highpoly_mesh.vertices(True):
            digram_mesh.add_vertex(key, x=attr['x'], y=attr['y'], z=attr['z'])

        for fkey in highpoly_mesh.face:
            digram_mesh.add_face(highpoly_mesh.face[fkey])

        return digram_mesh


def update_skeleton(skeleton):
    # this part should be embeded in UI

    while True:
        operation = rs.GetString('next')
        if operation == 'move_skeleton':
            skeleton.move_skeleton_vertex()
            skeleton.draw_self()
        elif operation == 'move_diagram':
            skeleton.move_diagram_vertext()
            skeleton.draw_self()
        elif operation == 'subdivide':
            skeleton.subdivide(k=1)
            skeleton.draw_self()
        elif operation == 'merge':
            skeleton.merge(k=1)
            skeleton.draw_self()
        elif operation == 'leaf_width':
            skeleton.dynamic_draw('leaf_width')
            skeleton.draw_self()
        elif operation == 'node_width':
            skeleton.dynamic_draw('node_width')
            skeleton.draw_self()

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
            skeleton.add_skeleton_lines(lines)
            skeleton.draw_self()

        elif operation == 'remove_lines':
            skeleton_branches = skeleton.skeleton_branches()
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

            skeleton.remove_skeleton_lines(remove_branches)
            skeleton.draw_self()

        elif operation == 'export':
            diagram = skeleton.to_diagram()
            mesh_draw_edges(diagram, layer='form diagram')
            mesh_draw_vertices(diagram, color=(0, 0, 255), layer='form diagram')
        elif operation == 'stop':
            rs.PurgeLayer('skeleton_vertices')
            break
        else:
            break


if __name__ == '__main__':

    line_ids = rs.GetObjects("select curves", filter=rs.filter.curve)
    lines = objects.get_line_coordinates(line_ids)
    rs.DeleteObjects(line_ids)

    skeleton = Skeleton.from_skeleton_lines(lines)
    skeleton.dynamic_draw_self()
    update_skeleton(skeleton)

    skeleton.to_json('skeleton_temp1.json', pretty=True)
