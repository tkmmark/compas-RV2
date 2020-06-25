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
        self._guid_reaction = {}
        self._guid_residual = {}
        self._guid_pipe = {}

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
        guids_reactions = list(self.guid_reaction.keys())
        guids_residuals = list(self.guid_residual.keys())
        guids_pipes = list(self.guid_pipe.keys())
        guids = guids_reactions + guids_residuals + guids_pipes
        delete_objects(guids, purge=True)
        self._guid_reaction = {}
        self._guid_residual = {}
        self._guid_pipe = {}

    def draw(self):
        layer = self.settings['layer']

        self.artist.layer = layer
        self.artist.clear_layer()

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)
        group_faces = "{}::faces".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if not compas_rhino.rs.IsGroup(group_faces):
            compas_rhino.rs.AddGroup(group_faces)

        # vertices

        guids_vertices = list(self.guid_vertex.keys())
        delete_objects(guids_vertices, purge=True)

        keys = list(self.datastructure.vertices())
        color = {key: self.settings['color.vertices'] for key in keys}
        color.update({key: self.settings['color.vertices:is_fixed'] for key in self.datastructure.vertices_where({'is_fixed': True}) if key in keys})
        color.update({key: self.settings['color.vertices:is_anchor'] for key in self.datastructure.vertices_where({'is_anchor': True}) if key in keys})

        guids = self.artist.draw_vertices(keys, color)
        self.guid_vertex = zip(guids, keys)

        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        if self.settings['show.vertices']:
            compas_rhino.rs.ShowGroup(group_vertices)
        else:
            compas_rhino.rs.HideGroup(group_vertices)

        # edges

        guids_edges = list(self.guid_edge.keys())
        delete_objects(guids_edges, purge=True)

        keys = list(self.datastructure.edges_where({'_is_edge': True}))
        color_edges = {key: self.settings['color.edges'] for key in keys}

        # color analysis

        # if self.scene.settings['RV2']['visualization.mode.force']:
        #     if self.datastructure.dual:
        #         _keys = list(self.datastructure.dual.edges())
        #         lengths = [self.datastructure.dual.edge_length(*key) for key in _keys]
        #         keys = [self.datastructure.dual.primal_edge(key) for key in _keys]
        #         lmin = min(lengths)
        #         lmax = max(lengths)
        #         for key, length in zip(keys, lengths):
        #             if lmin != lmax:
        #                 color_edges[key] = i_to_rgb((length - lmin) / (lmax - lmin))

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
        color = {key: self.settings['color.faces'] for key in keys}
        guids = self.artist.draw_faces(keys, color)
        self.guid_face = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_faces)

        if self.settings.get('show.faces', True):
            compas_rhino.rs.ShowGroup(group_faces)
        else:
            compas_rhino.rs.HideGroup(group_faces)

        # overlays

        if self.settings['show.reactions']:

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

        if self.settings['show.residuals']:

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

        if self.settings['show.pipes']:

            tol = self.settings['tol.pipes']
            keys = list(self.datastructure.edges_where({'_is_edge': True}))
            color = self.settings['color.pipes']
            # if self.scene.settings['RV2']['visualization.mode.force']:
            #     color = color_edges
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
