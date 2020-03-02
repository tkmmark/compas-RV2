from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ThrustDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoThrustDiagram
from compas_rv2.rhino import get_scene

__commandname__ = "RV2form_from_mesh"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    form = FormDiagram.from_rhinomesh(guid)
    thrust = form.copy(cls=ThrustDiagram)

    scene.clear()
    scene.add(form, name='form')
    scene.add(thrust, name='thrust')
    scene.update()

    # maybe the RV2 scene can be specialised for RV2

    # add form to data
    # store guids in scene nodes

    # adding data to a scene creates
    # node.artist
    # node.data
    # node.objects
    # => objects are created with artist based on data

    # rhinoform = RhinoFormDiagram(form)
    # rhinothrust = RhinoThrustDiagram(form)

    # rhinoform.draw(settings)

    # scene["form"] = rhinoform
    # scene["force"] = None
    # scene["thrust"] = rhinothrust


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
