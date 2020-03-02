from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.artists import Artist
import uuid


__all__ = ['Scene', 'SceneNode']


_ITEM_WRAPPER = {}


class SceneNode(object):

    def __init__(self, scene, item, **kwargs):
        self.scene = scene
        self.item = item
        self.artist = Artist.build(item, **kwargs)
        self.nodes = []


class Scene(object):

    def __init__(self, settings={}):
        self.nodes = {}
        self.settings = settings

    def add(self, item, name=None, **kwargs):
        node = Scene.build(item, **kwargs)
        _id = uuid.uuid4()
        self.nodes[_id] = node
        node.name = name
        return node

    def get(self, name):
        selected = []
        for _id in self.nodes:
            if name == self.nodes[_id].name:
                selected.append(self.nodes[_id])
        if len(selected) == 0:
            return None
        elif len(selected) == 1:
            return selected[0]
        else:
            return selected

    def update(self):
        compas_rhino.rs.EnableRedraw(False)
        for key in self.nodes:
            self.nodes[key].draw(self.settings)

    def clear(self):
        layers = [self.settings[name] for name in self.settings if name.startswith("layers")]
        compas_rhino.clear_layers(layers)
        #TODO: maybe clear and dispose each nodes first
        self.nodes = {}

    def update_settings(self, settings=None):
        return compas_rhino.update_settings(settings or self.settings)

    @staticmethod
    def register(item_type, wrapper_type):
        _ITEM_WRAPPER[item_type] = wrapper_type

    @staticmethod
    def build(item, **kwargs):
        wrapper = _ITEM_WRAPPER[type(item)]
        return wrapper(item, **kwargs)

    def to_data(self, include=None):
        if include is None:
            return {key: self.nodes[key].diagram.to_data() for key in self.nodes}
        else:
            data = {}
            for key in self.nodes:
                if key in include:
                    data[key] = self.nodes[key].diagram.to_data()
            return data


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Line
    from compas.geometry import Frame

    from compas.datastructures import Mesh

    scene = Scene()

    a = Point(1.0, 1.0, 0.0)
    b = Point(5.0, 5.0, 0.0)
    ab = Line(a, b)
    world = Frame.worldXY()

    mesh = Mesh.from_polyhedron(6)

    scene.add(a, name="A", color=(0, 0, 0), layer="A")
    scene.add(b, name="B", color=(255, 255, 255), layer="B")
    scene.add(ab, name="AB", color=(128, 128, 128), layer="AB")
    scene.add(world, name="World", layer="World")
    scene.add(mesh, name="Cube", layer="Cube")

    scene.update()
