from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ThrustArtist


__all__ = ["ThrustObject"]


class ThrustObject(MeshObject):

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
        return self._guid_reaction = {guid: key for key, guid in values}

    @property
    def guid_residual(self):
        return self._guid_residual

    @guid_residual.setter
    def guid_residual(self, values):
        return self._guid_residual = {guid: key for key, guid in values}

    @property
    def guid_pipe(self):
        return self._guid_pipe

    @guid_pipe.setter
    def guid_pipe(self, values):
        return self._guid_pipe = {guid: key for key, guid in values}

    def draw(self):
        layer = self.settings['thrust.layer']
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings['thrust.show.vertices']:
            keys = list(self.datastructure.vertices_where({'is_external': False}))
            color = {key: self.settings['thrust.color.vertices'] for key in keys}
            color.update({key: self.settings['thrust.color.vertices:is_fixed'] for key in self.datastructure.vertices_where({'is_fixed': True})})
            color.update({key: self.settings['thrust.color.vertices:is_anchor'] for key in self.datastructure.vertices_where({'is_anchor': True})})
            guids = self.artist.draw_vertices(keys, color)
            self.guid_vertex = zip(guids, keys)
        else:
            guids_vertices = list(self.guid_vertex.keys())
            compas_rhino.delete_objects(guids_vertices, purge=True)

        if self.settings['thrust.show.edges']:
            keys = list(self.datastructure.edges_where({'is_edge': True, 'is_external': False}))
            color = {key: self.settings['thrust.color.edges'] for key in keys}
            guids = self.artist.draw_edges(keys, color)
            self.guid_edge = zip(guids, keys)
        else:
            guids_edges = list(self.guid_edge.keys())
            compas_rhino.delete_objects(guids_edges, purge=True)

        if self.settings.get('thrust.show.faces', True):
            keys = list(self.datastructure.faces_where({'is_loaded': True}))
            color = {key: self.settings['thrust.color.faces'] for key in keys}
            guids = self.artist.draw_faces(keys, color)
            self.guid_face = zip(guids, keys)
        else:
            guids_faces = list(self.guid_face.keys())
            compas_rhino.delete_objects(guids_faces, purge=True)

        if self.settings['thrust.show.reactions']:
            keys = list(self.datastructure.vertices_where({'is_anchor': True}))
            color = self.settings['thrust.color.reactions']
            scale = self.settings['thrust.scale.reactions']
            guids = self.artist.draw_reactions(keys, color, scale)
            self.guid_reaction = zip(guids, keys)
        else:
            guids_reactions = list(self.guid_reaction.keys())
            compas_rhino.delete_objects(guids_reactions, purge=True)

        if self.settings['thrust.show.residuals']:
            keys = list(self.datastructure.vertices_where({'is_anchor': False, 'is_external': False}))
            color = self.settings['thrust.color.residuals']
            scale = self.settings['thrust.scale.residuals']
            guids = self.artist.draw_residuals(keys, color, scale)
            self.guid_residual = zip(guids, keys)
        else:
            guids_residuals = list(self.guid_residual)
            compas_rhino.delete_objects(guids_residuals, purge=True)

        if self.settings['thrust.show.pipes']:
            keys = list(self.datastructure.edges_where({'is_edge': True}))
            color = self.settings['thrust.color.pipes']
            scale = self.settings['thrust.scale.pipes']
            guids = self.artist.draw_pipes(keys, color, scale)
            self.guid_pipe = zip(guids, keys)
        else:
            guids_pipes = list(self.guid_pipe)
            compas_rhino.delete_objects(guids_pipes, purge=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
