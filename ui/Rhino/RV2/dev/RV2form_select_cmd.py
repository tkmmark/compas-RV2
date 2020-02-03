from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rhino.ui import CommandMenu


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
    "message": "FormDiagram Select",
    "options": [
        {"name": "Vertices", "message": "Select Vertices", "options": [
            {"name": "Boundary", "action": True},
            {"name": "Continuous", "action": True},
            {"name": "Parallel", "action": True},
        ]},
        # {"name": "Edges", "message": "Select Edges", "options": [
        #     {"name": "Boundary", "action": True},
        #     {"name": "Continuous", "action": True},
        #     {"name": "Parallel", "action": None},
        # ]},
        # {"name": "Faces", "message": "Select Faces", "options": [
        #     {"name": "Boundary", "action": None},
        #     {"name": "Continuous", "action": None},
        #     {"name": "Parallel", "action": None},
        # ]}
    ]
}


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    rhinoform = RV2["scene"]["form"]

    if not rhinoform:
        return

    settings = RV2["settings"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    if action["action"](rhinoform):
        rhinoform.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
