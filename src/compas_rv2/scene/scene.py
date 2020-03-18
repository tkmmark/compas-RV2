from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.artists import Artist
import uuid

from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ForceDiagram
from compas_rv2.diagrams import ThrustDiagram


__all__ = ['Scene',]


_ITEM_WRAPPER = {}


# class SceneNode(object):

#     def __init__(self, scene, item, **kwargs):
#         self.scene = scene
#         self.item = item
#         self.artist = Artist.build(item, **kwargs)
#         self.nodes = []


class Scene(object):

    def __init__(self, settings={}):
        self.nodes = {}
        self.settings = settings

    def add(self, item, name=None, visible=True, **kwargs):
        node = Scene.build(item, **kwargs)
        _id = uuid.uuid4()
        self.nodes[_id] = node
        node.name = name
        node.visible = visible
        return node

    def get(self, name):
        selected = []
        for _id in self.nodes:
            if name == self.nodes[_id].name:
                selected.append(self.nodes[_id])
        if len(selected) == 0:
            return None
        else:
            return selected

    def update(self):
        compas_rhino.rs.EnableRedraw(False)
        for key in self.nodes:
            node = self.nodes[key]
            if node.visible:
                node.draw(self.settings)
        compas_rhino.rs.EnableRedraw(True)

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
            data = {key: self.nodes[key].diagram.to_data() for key in self.nodes}
        else:
            data = {}
            for name in include:
                node = self.get(name)
                data[name] = node.diagram.to_data()
        data["settings"] = self.settings
        return data

    def from_data(self, data):
        # should this not be done explicitly by the user?
        self.clear()
        # this all seems extremely specific to the current case
        formdata = data.get("form")
        forcedata = data.get("force")
        settings = data.get("settings")
        if settings:
            self.settings = settings
        if formdata:
            form = FormDiagram.from_data(formdata)
            thrust = form.copy(cls=ThrustDiagram)
            self.add(form, name='form')
            self.add(thrust, name='thrust')
        if forcedata:
            force = ForceDiagram.from_data(forcedata)
            force.primal = form
            self.add(force, name='force')


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