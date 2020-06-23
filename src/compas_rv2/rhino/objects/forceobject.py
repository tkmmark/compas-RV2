from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import ForceArtist
from compas_rv2.rhino import delete_objects
from compas.utilities import i_to_rgb


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
        'layer': "RV2::ForceDiagram",
        'show.vertices': True,
        'show.edges': True,
        'show.angles': True,  # move to global settings?
        'show.color.analysis': False,  # temporary duplicate from formdiagram
        'color.vertices': [0, 255, 255],
        'color.vertices:is_fixed': [0, 255, 255],
        'color.edges': [0, 0, 255],
        'color.edges:is_external': [0, 0, 0],
        'tol.angles': 5  # temporary duplicate from formdiagram
    }

    def __init__(self, scene, diagram, **kwargs):
        super(ForceObject, self).__init__(scene, diagram, **kwargs)
        self.artist = ForceArtist(self.datastructure)

    def draw(self):
        """Draw the force diagram in Rhino using the current settings."""
        layer = self.settings["layer"]

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
        color = {key: self.settings["color.vertices"] for key in keys}
        guids = self.artist.draw_vertices(keys, color)
        self.guid_vertex = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        if self.settings["show.vertices"]:
            compas_rhino.rs.ShowGroup(group_vertices)
        else:
            compas_rhino.rs.HideGroup(group_vertices)

        # edges

        guids_edges = list(self.guid_edge.keys())
        delete_objects(guids_edges, purge=True)

        keys = list(self.datastructure.edges())
        color = {key: self.settings['color.edges'] for key in keys}
        for key in keys:
            key_ = self.datastructure.primal.face_adjacency_halfedge(*key)
            if self.datastructure.primal.edge_attribute(key_, '_is_external'):
                color[key] = self.settings["color.edges:is_external"]

        # color analysis

        if self.settings['show.color.analysis']:
            lengths = [self.datastructure.edge_length(*key) for key in keys]
            lmin = min(lengths)
            lmax = max(lengths)
            for key, length in zip(keys, lengths):
                if lmin != lmax:
                    color[key] = i_to_rgb((length - lmin) / (lmax - lmin))

        guids = self.artist.draw_edges(keys, color)
        self.guid_edge = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings["show.edges"]:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        # angles

        if self.settings['show.angles']:

            tol = self.settings['tol.angles']
            keys = list(self.datastructure.edges())
            angles = self.datastructure.edges_attribute('_a', keys=keys)
            amin = min(angles)
            amax = max(angles)
            if (amax - amin)**2 > 0.001**2:
                text = {}
                color = {}
                for key, angle in zip(keys, angles):
                    if angle > tol:
                        text[key] = "{:.0f}".format(angle)
                        color[key] = i_to_rgb((angle - amin) / (amax - amin))
                guids = self.artist.draw_edgelabels(text, color)
                self.guid_edgelabel = zip(guids, keys)

        else:
            guids_edgelabels = list(self.guid_edgelabel.keys())
            delete_objects(guids_edgelabels, purge=True)
            del self._guid_edgelabel
            self._guid_edgelabel = {}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
