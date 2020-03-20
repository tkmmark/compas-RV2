from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import MeshObject
from compas_rv2.rhino import FormArtist


__all__ = ["FormObject"]


class FormObject(MeshObject):

    def __init__(self, scene, diagram, **kwargs):
        super(FormObject, self).__init__(scene, diagram, **kwargs)
        self.artist = FormArtist(self.datastructure)
        self.vertex_attribute_editable('is_anchor', True)
        self.vertex_attribute_editable('is_fixed', True)
        self.vertex_attribute_editable('x', True)
        self.vertex_attribute_editable('y', True)

    def draw(self):
        layer = self.settings.get('form.layer')
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings.get('form.show.vertices', True):
            color = {}
            color.update({key: self.settings.get('form.color.vertices') for key in self.datastructure.vertices()})
            color.update({key: self.settings.get('form.color.vertices:is_fixed') for key in self.datastructure.vertices_where({'is_fixed': True})})
            color.update({key: self.settings.get('form.color.vertices:is_external') for key in self.datastructure.vertices_where({'is_external': True})})
            color.update({key: self.settings.get('form.color.vertices:is_anchor') for key in self.datastructure.vertices_where({'is_anchor': True})})
            self.guid_vertices = self.artist.draw_vertices(color=color)

        if self.settings.get('form.show.edges', True):
            keys = list(self.datastructure.edges_where({'is_edge': True}))
            color = {}
            color = {}
            for key in keys:
                u, v = key
                if self.datastructure.vertex_attribute(u, 'is_external') or self.datastructure.vertex_attribute(v, 'is_external'):
                    color[key] = self.settings.get('form.color.edges:is_external')
                else:
                    color[key] = self.settings.get('form.color.edges')
            self.guid_edges = self.artist.draw_edges(keys=keys, color=color)

        self.artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
