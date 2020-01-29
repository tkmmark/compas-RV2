from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import RhinoFormDiagram


__commandname__ = "RV2form_select"


HERE = compas_rhino.get_document_dirname()


def update_attributes_diagram(diagram):
    return diagram.update_attributes()


def update_attributes_vertices(diagram):
    return diagram.update_vertices_attributes()


def update_attributes_edges(diagram):
    return diagram.update_edges_attributes()


def update_attributes_faces(diagram):
    return diagram.update_faces_attributes()


config = {
    "message": "FormDiagram Attributes",
    "options": [
        {"name": "Diagram", "action": update_attributes_diagram},
        {"name": "Vertices", "action": update_attributes_vertices},
        {"name": "Edges", "action": update_attributes_edges},
        {"name": "Faces", "action": update_attributes_faces}
    ]
}


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    form = RV2["data"]["form"]

    if not form:
        return

    settings = RV2["settings"]

    diagram = RhinoFormDiagram(form)

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    if action["action"](diagram):
        diagram.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
