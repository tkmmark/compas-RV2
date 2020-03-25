from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import select_vertices as rv2_select_vertices
from compas_rv2.rhino import select_faces as rv2_select_faces
from compas_rv2.rhino import select_edges as rv2_select_edges
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier


__all__ = ['MeshObject']


class MeshObject(object):
    """Scene object for mesh-based data structures in RV2.

    Parameters
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    diagram : :class:`compas_rv2.datastructures.FormDiagram`
        The form diagram data structure.

    Attributes
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    diagram : :class:`compas_rv2.datastructures.FormDiagram`
        The form diagram data structure.
    name : str
        ...
    guid : str
        ...
    visible : bool
        ...
    settings : dict
        ...
    artist : :class:`compas_rv2.rhino.FormArtist`
        The specialised form diagram artist.

    Other Attributes
    ----------------
    guid_vertex : dict
        Dictionary mapping Rhino object GUIDs to data structure vertex identifiers.
    guid_edge : dict
        Dictionary mapping Rhino object GUIDs to data structure edge identifiers.
    guid_face : dict
        Dictionary mapping Rhino object GUIDs to data structure face identifiers.

    Notes
    -----
    Form diagrams have editable vertex attributes that can be modified
    by the user through the Rhino interface:

    * `x`: the X coordinate,
    * `y`: the Y coordinate, and
    * `z`: the Z coordinate.
    """

    __module__ = 'compas_rv2.rhino'

    def __init__(self, scene, datastructure, name=None, visible=True, **kwargs):
        self.scene = scene
        self.datastructure = datastructure
        self.name = name
        self.guid = None
        self.visible = visible
        self.artist = None
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}

    @property
    def settings(self):
        return self.scene.settings

    @property
    def guid_vertex(self):
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_vertexlabel(self):
        return self._guid_vertexlabel

    @guid_vertexlabel.setter
    def guid_vertexlabel(self, values):
        self._guid_vertexlabel = dict(values)

    @property
    def guid_facelabel(self):
        return self._guid_facelabel

    @guid_facelabel.setter
    def guid_facelabel(self, values):
        self._guid_facelabel = dict(values)

    @property
    def guid_edgelabel(self):
        return self._guid_edgelabel

    @guid_edgelabel.setter
    def guid_edgelabel(self, values):
        self._guid_edgelabel = dict(values)

    @property
    def guid_vertexnormal(self):
        return self._guid_vertexnormal

    @guid_vertexnormal.setter
    def guid_vertexnormal(self, values):
        self._guid_vertexnormal = dict(values)

    @property
    def guid_facenormal(self):
        return self._guid_facenormal

    @guid_facenormal.setter
    def guid_facenormal(self, values):
        self._guid_facenormal = dict(values)

    # ==========================================================================
    # Mesh
    # ==========================================================================

    def draw(self):
        raise NotImplementedError

    def clear(self):
        guids_vertices = list(self.guid_vertex.keys())
        guids_edges = list(self.guid_edge.keys())
        guids_faces = list(self.guid_face.keys())
        guids_vertexlabels = list(self.guid_vertexlabel.keys())
        guids_edgelabels = list(self.guid_edgelabel.keys())
        guids_facelabels = list(self.guid_facelabel.keys())
        guids_vertexnormals = list(self.guid_vertexnormal.keys())
        guids_facenormals = list(self.guid_facenormal.keys())
        guids = guids_vertices + guids_edges + guids_faces + guids_vertexlabels + guids_edgelabels + guids_facelabels + guids_vertexnormals + guids_facenormals
        compas_rhino.delete_objects(guids, purge=True)
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}

    def update_attributes(self):
        """Update the attributes of the data structure through a Rhino dialog.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        return compas_rhino.update_settings(self.datastructure.attributes)

    # ==========================================================================
    # Vertices
    # ==========================================================================

    def select_vertices(self):
        """Manually select vertices in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected vertices.

        Examples
        --------
        >>>
        """
        _filter = compas_rhino.rs.filter.point
        guids = compas_rhino.rs.GetObjects(message="Select Vertices.", preselect=True, select=True, group=False, filter=_filter)
        if guids:
            keys = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
        else:
            keys = []
        return keys

    def update_vertices_attributes(self, keys, names=None):
        """Update the attributes of selected vertices.

        Parameters
        ----------
        keys : list
            The identifiers of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is ``None``, in which case all attributes are updated.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        if keys:
            compas_rhino.rs.UnselectAllObjects()
            rv2_select_vertices(self.datastructure, keys)
            return VertexModifier.update_vertex_attributes(self.datastructure, keys, names)

    # ==========================================================================
    # Edges
    # ==========================================================================

    def select_edges(self):
        """Manually select edges in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected edges.

        Examples
        --------
        >>>
        """
        _filter = compas_rhino.rs.filter.curve
        guids = compas_rhino.rs.GetObjects(message="Select Edges.", preselect=True, select=True, group=False, filter=_filter)
        if guids:
            keys = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        else:
            keys = []
        return keys

    def update_edges_attributes(self, keys, names=None):
        """Update the attributes of selected edges.

        Parameters
        ----------
        keys : list
            The identifiers of the edges of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is ``None``, in which case all attributes are updated.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        if keys:
            compas_rhino.rs.UnselectAllObjects()
            rv2_select_edges(self.datastructure, keys)
            return EdgeModifier.update_edge_attributes(self.datastructure, keys, names)

    # ==========================================================================
    # Faces
    # ==========================================================================

    def select_faces(self):
        """Manually select faces in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected faces.

        Examples
        --------
        >>>
        """
        _filter = compas_rhino.rs.filter.mesh
        guids = compas_rhino.rs.GetObjects(message="Select Faces.", preselect=True, select=True, group=False, filter=_filter)
        if guids:
            keys = [self.guid_face[guid] for guid in guids if guid in self.guid_face]
        else:
            keys = []
        return keys

    def update_faces_attributes(self, keys, names=None):
        """Update the attributes of selected faces.

        Parameters
        ----------
        keys : list
            The identifiers of the faces of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is ``None``, in which case all attributes are updated.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        if keys:
            compas_rhino.rs.UnselectAllObjects()
            rv2_select_faces(self.datastructure, keys)
            return FaceModifier.update_face_attributes(self.datastructure, keys, names)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
