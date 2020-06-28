from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ThrustArtist
from compas_rv2.rhino import delete_objects


__all__ = ["ThrustObject"]


class ThrustObject(MeshObject):

    settings = {
        'layer': "RV2::ThrustDiagram",
        '_is.valid': False,
        'show.vertices': False,
        'show.edges': False,
        'show.faces': True,
        'show.reactions': True,
        'show.residuals': False,
        'show.selfweight': False,
        'show.loads': False,
        'show.pipes': False,
        'color.vertices': [255, 0, 255],
        'color.vertices:is_fixed': [0, 255, 0],
        'color.vertices:is_anchor': [255, 0, 0],
        'color.edges': [255, 0, 255],
        'color.faces': [255, 0, 255],
        'color.reactions': [0, 80, 0],
        'color.residuals': [0, 255, 255],
        'color.pipes': [0, 0, 255],
        'color.invalid': [100, 255, 100],
        'scale.reactions': 0.1,
        'scale.residuals': 1.0,
        'scale.pipes': 0.01,
        'tol.reactions': 1e-3,
        'tol.residuals': 1e-3,
        'tol.pipes': 1e-3,
    }

    def __init__(self, scene, diagram, **kwargs):
        super(ThrustObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ThrustArtist(self.datastructure)
        self._guid_vertex_free = {}
        self._guid_vertex_anchor = {}
        self._guid_reaction = {}
        self._guid_residual = {}
        self._guid_pipe = {}

    @property
    def guid_vertex_free(self):
        return self._guid_vertex_free

    @guid_vertex_free.setter
    def guid_vertex_free(self, values):
        self._guid_vertex_free = dict(values)

    @property
    def guid_vertex_anchor(self):
        return self._guid_vertex_anchor

    @guid_vertex_anchor.setter
    def guid_vertex_anchor(self, values):
        self._guid_vertex_anchor = dict(values)

    @property
    def guid_reaction(self):
        return self._guid_reaction

    @guid_reaction.setter
    def guid_reaction(self, values):
        self._guid_reaction = dict(values)

    @property
    def guid_residual(self):
        return self._guid_residual

    @guid_residual.setter
    def guid_residual(self, values):
        self._guid_residual = dict(values)

    @property
    def guid_pipe(self):
        return self._guid_pipe

    @guid_pipe.setter
    def guid_pipe(self, values):
        self._guid_pipe = dict(values)

    def clear(self):
        super(ThrustObject, self).clear()
        guids_vertices_free = list(self.guid_vertex_free.keys())
        guids_vertices_anchor = list(self.guid_vertex_anchor.keys())
        guids_reactions = list(self.guid_reaction.keys())
        guids_residuals = list(self.guid_residual.keys())
        guids_pipes = list(self.guid_pipe.keys())
        guids = guids_reactions + guids_residuals + guids_pipes + guids_vertices_free + guids_vertices_anchor
        delete_objects(guids, purge=True)
        self._guid_vertex_free = {}
        self._guid_vertex_anchor = {}
        self._guid_reaction = {}
        self._guid_residual = {}
        self._guid_pipe = {}

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
            guid_vertex = {}
            guid_vertex.update(self.guid_vertex_free)
            guid_vertex.update(self.guid_vertex_anchor)
            keys = [guid_vertex[guid] for guid in guids if guid in guid_vertex]
        else:
            keys = []
        return keys

    def select_vertices_free(self):
        """Manually select free vertices in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected vertices.

        Examples
        --------
        >>>
        """
        _filter = compas_rhino.rs.filter.point
        guids = compas_rhino.rs.GetObjects(message="Select Free Vertices.", preselect=True, select=True, group=False, filter=_filter)
        if guids:
            keys = [self.guid_vertex_free[guid] for guid in guids if guid in self.guid_vertex_free]
        else:
            keys = []
        return keys

    def select_vertices_anchor(self):
        """Manually select anchor vertices in the Rhino model view.

        Returns
        -------
        list
            The keys of the selected vertices.

        Examples
        --------
        >>>
        """
        _filter = compas_rhino.rs.filter.point
        guids = compas_rhino.rs.GetObjects(message="Select Anchor Vertices.", preselect=True, select=True, group=False, filter=_filter)
        if guids:
            keys = [self.guid_vertex_anchor[guid] for guid in guids if guid in self.guid_vertex_anchor]
        else:
            keys = []
        return keys

    def draw(self):
        layer = self.settings['layer']

        self.artist.layer = layer
        self.artist.clear_layer()

        group_vertices_free = "{}::vertices_free".format(layer)
        group_vertices_anchor = "{}::vertices_anchor".format(layer)

        group_edges = "{}::edges".format(layer)
        group_faces = "{}::faces".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices_free):
            compas_rhino.rs.AddGroup(group_vertices_free)

        if not compas_rhino.rs.IsGroup(group_vertices_anchor):
            compas_rhino.rs.AddGroup(group_vertices_anchor)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if not compas_rhino.rs.IsGroup(group_faces):
            compas_rhino.rs.AddGroup(group_faces)

        # vertices

        guids_vertices_free = list(self.guid_vertex_free.keys())
        guids_vertices_anchor = list(self.guid_vertex_anchor.keys())
        delete_objects(guids_vertices_free + guids_vertices_anchor, purge=True)

        free = list(self.datastructure.vertices_where({'is_anchor': False}))
        anchors = list(self.datastructure.vertices_where({'is_anchor': True}))

        color_free = self.settings['color.vertices'] if self.settings['_is.valid'] else self.settings['color.invalid']
        color_anchor = self.settings['color.vertices:is_anchor']

        color = {key: color_free for key in free}
        color.update({key: color_anchor for key in anchors})

        guids_vertices_free = self.artist.draw_vertices(free, color)
        self.guid_vertex_free = zip(guids_vertices_free, free)

        guids_vertices_anchor = self.artist.draw_vertices(anchors, color)
        self.guid_vertex_anchor = zip(guids_vertices_anchor, anchors)

        compas_rhino.rs.AddObjectsToGroup(guids_vertices_free, group_vertices_free)
        compas_rhino.rs.AddObjectsToGroup(guids_vertices_anchor, group_vertices_anchor)

        if self.settings['show.vertices']:
            compas_rhino.rs.HideGroup(group_vertices_free)
            compas_rhino.rs.ShowGroup(group_vertices_anchor)
        else:
            compas_rhino.rs.HideGroup(group_vertices_free)
            compas_rhino.rs.HideGroup(group_vertices_anchor)

        # edges

        guids_edges = list(self.guid_edge.keys())
        delete_objects(guids_edges, purge=True)

        keys = list(self.datastructure.edges_where({'_is_edge': True}))
        color_edges = {key: self.settings['color.edges'] if self.settings['_is.valid'] else self.settings['color.invalid'] for key in keys}

        guids = self.artist.draw_edges(keys, color_edges)
        self.guid_edge = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings['show.edges']:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        # faces

        guids_faces = list(self.guid_face.keys())
        delete_objects(guids_faces, purge=True)

        keys = list(self.datastructure.faces_where({'_is_loaded': True}))
        color = {key: self.settings['color.faces'] if self.settings['_is.valid'] else self.settings['color.invalid'] for key in keys}
        guids = self.artist.draw_faces(keys, color)
        self.guid_face = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_faces)

        if self.settings.get('show.faces', True):
            compas_rhino.rs.ShowGroup(group_faces)
        else:
            compas_rhino.rs.HideGroup(group_faces)

        # overlays

        if self.settings['_is.valid'] and self.settings['show.reactions']:

            tol = self.settings['tol.reactions']
            anchors = list(self.datastructure.vertices_where({'is_anchor': True}))
            fixed = list(self.datastructure.vertices_where({'is_fixed': True}))
            keys = list(set(anchors + fixed))
            color = self.settings['color.reactions']
            scale = self.settings['scale.reactions']
            guids = self.artist.draw_reactions(keys, color, scale, tol)
            self.guid_reaction = zip(guids, keys)

        else:
            guids_reactions = list(self.guid_reaction.keys())
            delete_objects(guids_reactions, purge=True)
            del self._guid_reaction
            self._guid_reaction = {}

        if self.settings['_is.valid'] and self.settings['show.residuals']:

            tol = self.settings['tol.residuals']
            keys = list(self.datastructure.vertices_where({'is_anchor': False, 'is_fixed': False}))
            color = self.settings['color.residuals']
            scale = self.settings['scale.residuals']
            guids = self.artist.draw_residuals(keys, color, scale, tol)
            self.guid_residual = zip(guids, keys)

        else:
            guids_residuals = list(self.guid_residual)
            delete_objects(guids_residuals, purge=True)
            del self._guid_residual
            self._guid_residual = {}

        if self.settings['_is.valid'] and self.settings['show.pipes']:

            tol = self.settings['tol.pipes']
            keys = list(self.datastructure.edges_where({'_is_edge': True}))
            color = self.settings['color.pipes']
            scale = self.settings['scale.pipes']
            guids = self.artist.draw_pipes(keys, color, scale, tol)
            self.guid_pipe = zip(guids, keys)

        else:
            guids_pipes = list(self.guid_pipe)
            delete_objects(guids_pipes, purge=True)
            del self._guid_pipe
            self._guid_pipe = {}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
