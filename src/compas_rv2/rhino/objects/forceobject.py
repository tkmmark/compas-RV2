from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ForceArtist
from compas_rv2.rhino import delete_objects


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

    settings = {
        'force.layer': "RV2::ForceDiagram",
        'force.show.vertices': False,
        'force.show.edges': True,
        'force.color.vertices': [0, 255, 0],
        'force.color.vertices:is_fixed': [0, 255, 255],
        'force.color.edges': [0, 255, 0],
        'force.color.edges:is_external': [0, 0, 255],
    }

    def __init__(self, scene, diagram, **kwargs):
        super(ForceObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ForceArtist(self.datastructure)

    def draw(self):
        """Draw the force diagram in Rhino using the current settings."""
        layer = self.settings["force.layer"]

        self.artist.layer = layer
        self.artist.clear_layer()

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        # vertices

        guids_vertices = list(self.guid_vertex.keys())
        delete_objects(guids_vertices, purge=True)

        keys = list(self.datastructure.vertices())
        color = {key: self.settings["force.color.vertices"] for key in keys}
        guids = self.artist.draw_vertices(keys, color)
        self.guid_vertex = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        if self.settings["force.show.vertices"]:
            compas_rhino.rs.ShowGroup(group_vertices)
        else:
            compas_rhino.rs.HideGroup(group_vertices)

        # edges

        guids_edges = list(self.guid_edge.keys())
        delete_objects(guids_edges, purge=True)

        keys = list(self.datastructure.edges())
        color = {key: self.settings['force.color.edges'] for key in keys}
        for key in keys:
            key_ = self.datastructure.primal.face_adjacency_halfedge(*key)
            if self.datastructure.primal.edge_attribute(key_, '_is_external'):
                color[key] = self.settings["force.color.edges:is_external"]
        guids = self.artist.draw_edges(keys, color)
        self.guid_edge = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings["force.show.edges"]:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass