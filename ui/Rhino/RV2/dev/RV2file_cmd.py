from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino
from compas_rhino.ui import CommandMenu

from compas_rv2 import FormDiagram

from commands import open_file
from commands import save_file
from commands import saveas_file

HERE = compas_rhino.get_document_dirname()
HERE = HERE or os.path.dirname(compas_fofin.__file__)


__commandname__ = "RV2file"


config = {
    "name": "file",
    "message": "File",
    "options": [
        {
            "name": "open",
            "message": "Open",
            "action": open_file
        },
        {
            "name": "save",
            "message": "Save",
            "action": save_file
        },
        {
            "name": "saveas",
            "message": "Save As",
            "action": saveas_file
        }
    ]
}


def RunCommand(is_interactive):
    # can this be moved to a decorator
    if "RV2" not in sc.sticky:
        raise Exception("Initialise the plugin first!")

    RV2 = sc.sticky["RV2"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if action:
        action(RV2)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
