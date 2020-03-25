from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ThrustArtist


__all__ = ["ThrustObject"]


class ThrustObject(MeshObject):

    def __init__(self, scene, diagram, settings={}, **kwargs):
        super(ThrustObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ThrustArtist(self.datastructure)
        self._guid_reaction = {}
        self._guid_residual = {}
        self._guid_pipe = {}
        self.settings = {
            'show.vertices': False,
            'show.edges': True,
            'show.faces': True,
            'show.reactions': True,
            'show.residuals': False,
            'show.pipes': True,
            'color.vertices': [255, 0, 255],
            'color.vertices:is_fixed': [0, 255, 0],
            'color.vertices:is_anchor': [255, 0, 0],
            'color.edges': [255, 0, 255],
            'color.faces': [255, 0, 255],
            'color.reactions': [0, 255, 255],
            'color.residuals': [0, 255, 255],
            'color.pipes': [0, 0, 255],
            'scale.reactions': 0.1,
            'scale.residuals': 1.0,
            'scale.pipes': 0.01,
            'layer': "RV2::ThrustDiagram"
        }
        self.settings.update(settings)

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

    def draw(self):
        layer = self.settings['layer']
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings['show.vertices']:
            keys = list(self.datastructure.vertices_where({'_is_external': False}))
            color = {key: self.settings['color.vertices'] for key in keys}
            color.update({key: self.settings['color.vertices:is_fixed'] for key in self.datastructure.vertices_where({'is_fixed': True}) if key in keys})
            color.update({key: self.settings['color.vertices:is_anchor'] for key in self.datastructure.vertices_where({'is_anchor': True}) if key in keys})
            guids = self.artist.draw_vertices(keys, color)
            self.guid_vertex = zip(guids, keys)
        else:
            guids_vertices = list(self.guid_vertex.keys())
            compas_rhino.delete_objects(guids_vertices, purge=True)
            self._guid_vertex = {}

        if self.settings['show.edges']:
            keys = list(self.datastructure.edges_where({'_is_edge': True, '_is_external': False}))
            color = {key: self.settings['color.edges'] for key in keys}
            guids = self.artist.draw_edges(keys, color)
            self.guid_edge = zip(guids, keys)
        else:
            guids_edges = list(self.guid_edge.keys())
            compas_rhino.delete_objects(guids_edges, purge=True)
            self._guid_edge = {}

        if self.settings.get('show.faces', True):
            keys = list(self.datastructure.faces_where({'_is_loaded': True}))
            color = {key: self.settings['color.faces'] for key in keys}
            guids = self.artist.draw_faces(keys, color)
            self.guid_face = zip(guids, keys)
        else:
            guids_faces = list(self.guid_face.keys())
            compas_rhino.delete_objects(guids_faces, purge=True)
            self._guid_face = {}

        if self.settings['show.reactions']:
            keys = list(self.datastructure.vertices_where({'is_anchor': True}))
            color = self.settings['color.reactions']
            scale = self.settings['scale.reactions']
            guids = self.artist.draw_reactions(keys, color, scale)
            self.guid_reaction = zip(guids, keys)
        else:
            guids_reactions = list(self.guid_reaction.keys())
            compas_rhino.delete_objects(guids_reactions, purge=True)
            self._guid_reaction = {}

        if self.settings['show.residuals']:
            keys = list(self.datastructure.vertices_where({'is_anchor': False, '_is_external': False}))
            color = self.settings['color.residuals']
            scale = self.settings['scale.residuals']
            guids = self.artist.draw_residuals(keys, color, scale)
            self.guid_residual = zip(guids, keys)
        else:
            guids_residuals = list(self.guid_residual)
            compas_rhino.delete_objects(guids_residuals, purge=True)
            self._guid_residual = {}

        # if self.settings['show.pipes']:
        #     keys = list(self.datastructure.edges_where({'_is_edge': True}))
        #     color = self.settings['color.pipes']
        #     scale = self.settings['scale.pipes']
        #     guids = self.artist.draw_pipes(keys, color, scale)
        #     self.guid_pipe = zip(guids, keys)
        # else:
        #     guids_pipes = list(self.guid_pipe)
        #     compas_rhino.delete_objects(guids_pipes, purge=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
