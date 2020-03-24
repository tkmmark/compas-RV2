from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import FormArtist


__all__ = ["FormObject"]


class FormObject(MeshObject):
    """Scene object for RV2 form diagrams.

    Parameters
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    diagram : :class:`compas_rv2.datastructures.FormDiagram`
        The form diagram data structure.

    Attributes
    ----------
    artist : :class:`compas_rv2.rhino.FormArtist`
        The specialised form diagram artist.

    Notes
    -----
    Form diagrams have editable vertex attributes that can be modified
    by the user through the Rhino interface:

    * `is_anchor`: flag for marking a vertex as anchored,
    * `is_fixed`: flag for marking a vertex as fixed,
    * `x`: the X coordinate, and
    * `y`: the Y coordinate.

    Examples
    --------
    >>> form = FormDiagram.from_pattern(pattern)
    >>> scene = Scene()
    >>> scene.settings = {... this should be stuff related to the scene, not to the settings of individual nodes ...}
    >>> node = scene.add(force, name='form', settings=settings)
    >>> scene.update()
    >>> node.settings['show.vertices'] = True
    >>> node.settings['color.vertices'] = {key: (255, 0, 0) for key in node.datastructure.vertices_wehere({'is_fixed': True})}
    >>> scene.update()
    """

    __module__ = 'compas_rv2.rhino'

    def __init__(self, scene, diagram, **kwargs):
        super(FormObject, self).__init__(scene, diagram, **kwargs)
        self.artist = FormArtist(self.datastructure)

    def draw(self):
        """Draw the form diagram in the Rhino scene using the current settings."""
        layer = self.settings['form.layer']
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings['form.show.vertices']:
            keys = list(self.datastructure.vertices())
            color = {key: self.settings['form.color.vertices'] for key in keys}
            color.update({key: self.settings['form.color.vertices:is_fixed'] for key in self.datastructure.vertices_where({'is_fixed': True})})
            color.update({key: self.settings['form.color.vertices:is_external'] for key in self.datastructure.vertices_where({'is_external': True})})
            color.update({key: self.settings['form.color.vertices:is_anchor'] for key in self.datastructure.vertices_where({'is_anchor': True})})
            guids = self.artist.draw_vertices(keys, color)
            self.guid_vertex = zip(guids, keys)
        else:
            guids_vertices = list(self.guid_vertex.keys())
            compas_rhino.delete_objects(guids_vertices, purge=True)

        if self.settings['form.show.edges']:
            keys = list(self.datastructure.edges_where({'is_edge': True}))
            color = {key: self.settings['form.color.edges'] for key in keys}
            color.update({key: self.settings['form.color.edges:is_external'] for key in self.datastructure.edges_where({'is_external': True})})
            guids = self.artist.draw_edges(keys, color)
            self.guid_edge = zip(guids, keys)
        else:
            guids_edges = list(self.guid_edge.keys())
            compas_rhino.delete_objects(guids_edges, purge=True)

        # if self.settings['form.show.angles']:
        #     keys = list()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
