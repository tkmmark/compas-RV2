from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ForceArtist


__all__ = ["ForceObject"]


class ForceObject(MeshObject):
    """Scene object for RV2 force diagrams.

    Parameters
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    diagram : :class:`compas_rv2.datastructures.ForceDiagram`
        The force diagram data structure.

    Attributes
    ----------
    artist : :class:`compas_rv2.rhino.ForceArtist`
        The specialised force diagram artist.

    Notes
    -----
    Force diagrams have two editable vertex attributes that can be modified
    by the user through the Rhino interface:

    * `x`: the X coordinate
    * `y`: the Y coordinate.

    Examples
    --------
    >>> form = ...
    >>> force = ForceDiagram.from_formdiagram(form)
    >>> scene = Scene()
    >>> scene.settings = {... this should be stuff related to the scene, not to the settings of individual nodes ...}
    >>> node = scene.add(force, name='force', settings=settings)
    >>> scene.update()
    >>> node.settings['show.vertices'] = True
    >>> node.settings['color.vertices'] = {key: (255, 0, 0) for key in node.datastructure.vertices_wehere({'is_fixed': True})}
    >>> scene.update()
    """

    __module__ = 'compas_rv2.rhino'

    def __init__(self, scene, diagram, **kwargs):
        super(ForceObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ForceArtist(self.datastructure)

    def draw(self):
        """Draw the force diagram in Rhino using the current settings."""
        layer = self.settings["force.layer"]
        if layer:
            self.artist.layer = layer
            self.artist.clear_layer()

        if self.settings["force.show.vertices"]:
            keys = list(self.datastructure.vertices())
            color = {key: self.settings["force.color.vertices"] for key in keys}
            guids = self.artist.draw_vertices(keys, color)
            self.guid_vertex = zip(guids, keys)
        else:
            guids_vertices = list(self.guid_vertex.keys())
            compas_rhino.delete_objects(guids_vertices, purge=True)
            self._guid_vertex = {}

        if self.settings["force.show.edges"]:
            keys = list(self.datastructure.edges())
            color = {key: self.settings['force.color.edges'] for key in keys}
            for key in keys:
                key_ = self.datastructure.primal.face_adjacency_halfedge(*key)
                if self.datastructure.primal.edge_attribute(key_, '_is_external'):
                    color[key] = self.settings["force.color.edges:is_external"]
            guids = self.artist.draw_edges(keys, color)
            self.guid_edge = zip(guids, keys)
        else:
            guids_edges = list(self.guid_edge.keys())
            compas_rhino.delete_objects(guids_edges, purge=True)
            self._guid_edge = {}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
