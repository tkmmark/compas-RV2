from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import cos
from math import sin

from compas.geometry import add_vectors_xy
from compas.geometry import subtract_vectors_xy
from compas.geometry import normalize_vector_xy
from compas.geometry import angle_vectors_xy
from compas.geometry import cross_vectors
from compas.geometry import scale_vector

from compas_tna.diagrams import FormDiagram
from compas_rv2.datastructures.meshmixin import MeshMixin


__all__ = ['FormDiagram']


def rotate(point, angle):
    x = cos(angle) * point[0] - sin(angle) * point[1]
    y = sin(angle) * point[0] + cos(angle) * point[1]
    return x, y, 0


def cross_z(ab, ac):
    return ab[0] * ac[1] - ab[1] * ac[0]


class FormDiagram(MeshMixin, FormDiagram):
    """The RV2 FormDiagram.

    Examples
    --------
    The :class:`FormDiagram` is constructed from a :class:`Pattern`.
    The pattern defines the directions along which (horizontal) forces can flow
    through the funicular network.

    >>> form = FormDiagram.from_pattern(pattern)

    In order for the pattern to be valid input for making a form diagram,
    it should define both the geometry and the boundary conditions of the problem.
    """

    @classmethod
    def from_pattern(cls, pattern, feet=2):
        """Construct a form diagram from a pattern.

        Parameters
        ----------
        pattern : Pattern
            The pattern from which the diagram should be constructed.
        feet : {1, 2}, optional
            The number of horizontal force directions that should be added to the supports.

        Returns
        -------
        FormDiagram
            The form diagram.
        """
        form = pattern.copy(cls=cls)
        form.update_boundaries()
        return form

    def update_boundaries(self):
        # split boundaries on anchors
        # add feet (corresponding new faces, mark has_external, is_external)
        # mark faces

        scale = self.attributes['feet.scale']
        alpha = pi * 45 / 180
        tol = self.attributes['feet.tol']

        # mark all "anchored edges" as '_is_edge=False'
        for edge in self.edges():
            self.edge_attribute(edge, '_is_edge', not all(self.vertices_attribute('is_anchor', keys=edge)))

        # outer boundary
        # note: how to make sure this is the "outer" boundary
        boundaries = self.vertices_on_boundaries()
        exterior = boundaries[0]

        # split outer boundary
        # where `is_anchor=True`
        # into (ordered) series of boundary edges
        segment = []
        segments = [segment]
        for vertex in exterior:
            segment.append(vertex)
            if self.vertex_attribute(vertex, 'is_anchor'):
                segment = [vertex]
                segments.append(segment)
        segments[-1] += segments[0]
        del segments[0]

        # add new vertices
        # where number of `_is_edge=True` connected edges at begin/end vertices of a segment is greater than 1
        key_foot = {}
        key_xyz = {key: self.vertex_coordinates(key, 'xyz') for key in self.vertices()}

        for i, vertices in enumerate(segments):
            key = vertices[0]
            nbrs = self.vertex_neighbors(key)

            count = 0
            for nbr in nbrs:
                edge = key, nbr
                if self.edge_attribute(edge, '_is_edge'):
                    count += 1

            if count > 1:
                after = vertices[1]
                before = segments[i - 1][-2]

                # base point
                o = key_xyz[key]

                # +normal
                b = key_xyz[before]
                a = key_xyz[after]
                ob = normalize_vector_xy(subtract_vectors_xy(b, o))
                oa = normalize_vector_xy(subtract_vectors_xy(a, o))
                z = cross_z(ob, oa)
                if z > +tol:
                    n = normalize_vector_xy(add_vectors_xy(oa, ob))
                    n = scale_vector(n, -scale)
                elif z < -tol:
                    n = normalize_vector_xy(add_vectors_xy(oa, ob))
                    n = scale_vector(n, +scale)
                else:
                    ba = normalize_vector_xy(subtract_vectors_xy(a, b))
                    n = cross_vectors([0, 0, 1], ba)
                    n = scale_vector(n, +scale)

                # left and right
                lx, ly, lz = add_vectors_xy(o, rotate(n, +alpha))
                rx, ry, rz = add_vectors_xy(o, rotate(n, -alpha))
                l = self.add_vertex(x=lx, y=ly, z=o[2], is_fixed=True, _is_external=True)
                r = self.add_vertex(x=rx, y=ry, z=o[2], is_fixed=True, _is_external=True)
                key_foot[key] = l, r

                # foot face
                self.add_face([l, key, r], _is_loaded=False)

                # foot face attributes
                self.edge_attribute((l, key), '_is_external', True)
                self.edge_attribute((key, r), '_is_external', True)
                self.edge_attribute((r, l), '_is_edge', False)

        # add (opening?) faces

        for vertices in segments:
            if len(vertices) < 3:
                continue

            left = vertices[0]
            right = vertices[-1]

            start = None
            end = None

            if left in key_foot:
                start = key_foot[left][1]

            if right in key_foot:
                end = key_foot[right][0]

            if start is not None:
                vertices.insert(0, start)
            if end is not None:
                vertices.append(end)
            self.add_face(vertices, _is_loaded=False)
            self.edge_attribute((vertices[0], vertices[-1]), '_is_edge', False)

        # # mark all faces with at least one external vertex (`_is_external=True`) as `_is_loaded/_is_face=False`
        # for face in self.faces():
        #     self.face_attribute(face, '_is_loaded', any(self.vertices_attribute('_is_external', keys=self.face_vertices(face))))

    def dual_edge(self, key):
        """Get the corresponding edge in the ForceDiagram.

        Parameters
        ----------
        key : tuple
            The identifier of the edge in this diagram.

        Returns
        -------
        tuple
            The identifier of the edge in the other/dual diagram.

        Raises
        ------
        KeyError
            If the dual edge does not exist.
        """
        f1, f2 = key
        for u, v in self.dual.face_halfedges(f1):
            if self.dual.halfedge[v][u] == f2:
                return u, v

        raise KeyError(key)

    def update_angle_deviations(self):
        """Compute the angle deviation with the corresponding edge in the ForceDiagram.
        """
        for key in self.edges_where({'_is_external': False, '_is_edge': True}):
            uv = self.edge_vector(key[0], key[1])
            _key = self.dual_edge(key)
            _uv = self.dual.edge_vector(_key[0], _key[1])
            a = angle_vectors_xy(uv, cross_vectors((0, 0, 1), _uv), deg=True)
            self.edge_attribute(key, '_a', a)
            self.dual.edge_attribute(_key, '_a', a)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
