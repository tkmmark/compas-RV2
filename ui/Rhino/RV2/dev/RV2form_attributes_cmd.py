from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rhino.ui import CommandMenu

__commandname__ = "RV2form_attributes"


HERE = compas_rhino.get_document_dirname()


def update_attributes_diagram(diagram):
    return diagram.update_attributes()


def update_attributes_vertices(diagram):
    return diagram.update_vertices_attributes()


def update_attributes_edges(diagram):
    return diagram.update_edges_attributes()


def update_attributes_faces(diagram):
    return diagram.update_faces_attributes()


def property_sheet(diagram):
    propertySheet = PropertySheet()
    propertySheet.setup(diagram)
    propertySheet.Show()
    sc.sticky["RV2"]["propertySheet"] = propertySheet
    return False


def goto_selection(diagram):
    propertySheet = sc.sticky["RV2"]["propertySheet"]
    # propertySheet.Enabled = True
    # propertySheet.Visible = True
    propertySheet.vertices_table.SelectRow(2)
    return False


def redraw(diagram):
    return True


config = {
    "message": "FormDiagram Attributes",
    "options": [
        {"name": "Diagram", "action": update_attributes_diagram},
        {"name": "Vertices", "action": update_attributes_vertices},
        {"name": "Edges", "action": update_attributes_edges},
        {"name": "Faces", "action": update_attributes_faces},
        {"name": "Property", "action": property_sheet},
        {"name": "redraw", "action": redraw},
        {"name": "goto_selection", "action": goto_selection},


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
