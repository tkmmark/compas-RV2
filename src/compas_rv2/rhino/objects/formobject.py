from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import FormArtist
from compas.utilities import i_to_green


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

        self.artist.layer = layer
        self.artist.clear_layer()

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if self.settings['form.show.vertices']:

            keys = list(self.datastructure.vertices())
            color = {key: self.settings['form.color.vertices'] for key in keys}
            color_fixed = self.settings['form.color.vertices:is_fixed']
            color_external = self.settings['form.color.vertices:is_external']
            color_anchor = self.settings['form.color.vertices:is_anchor']
            color.update({key: color_fixed for key in self.datastructure.vertices_where({'is_fixed': True}) if key in keys})
            color.update({key: color_external for key in self.datastructure.vertices_where({'_is_external': True}) if key in keys})
            color.update({key: color_anchor for key in self.datastructure.vertices_where({'is_anchor': True}) if key in keys})
            guids = self.artist.draw_vertices(keys, color)
            self.guid_vertex = zip(guids, keys)
            compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        else:
            guids_vertices = list(self.guid_vertex.keys())
            compas_rhino.delete_objects(guids_vertices, purge=True)
            compas_rhino.rs.DeleteGroup(group_vertices)
            del self._guid_vertex
            self._guid_vertex = {}

        if self.settings['form.show.edges']:

            keys = list(self.datastructure.edges_where({'_is_edge': True}))
            color = {key: self.settings['form.color.edges'] for key in keys}
            color.update({key: self.settings['form.color.edges:is_external'] for key in self.datastructure.edges_where({'_is_external': True})})
            guids = self.artist.draw_edges(keys, color)
            self.guid_edge = zip(guids, keys)
            compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        else:
            guids_edges = list(self.guid_edge.keys())
            compas_rhino.delete_objects(guids_edges, purge=True)
            compas_rhino.rs.DeleteGroup(group_edges)
            del self._guid_edge
            self._guid_edge = {}

        if self.settings['form.show.angles']:

            tol = self.settings['form.tol.angles']
            keys = list(self.datastructure.edges_where({'_is_edge': True}))
            angles = self.datastructure.edges_attribute('_a', keys=keys)
            amin = min(angles)
            amax = max(angles)
            if (amax - amin)**2 > 0.001**2:
                text = {}
                color = {}
                for key, angle in zip(keys, angles):
                    if angle > tol:
                        text[key] = "{:.0f}".format(angle)
                        color[key] = i_to_green((angle - amin) / (amax - amin))
                guids = self.artist.draw_edgelabels(text, color)
                self.guid_edgelabel = zip(guids, keys)

        else:
            guids_edgelabels = list(self.guid_edgelabel.keys())
            compas_rhino.delete_objects(guids_edgelabels, purge=True)
            del self._guid_edgelabel
            self._guid_edgelabel = {}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
