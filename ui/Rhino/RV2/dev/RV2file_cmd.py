from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

import scriptcontext as sc

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rhino.etoforms import TextForm
from compas.utilities import DataEncoder
from compas.utilities import DataDecoder
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoForceDiagram
from compas_rv2.rhino import RhinoThrustDiagram


__commandname__ = "RV2file"


HERE = compas_rhino.get_document_dirname()


def is_session_file(filepath, ext):
    if not filepath:
        return False
    if not os.path.exists(filepath):
        return False
    if not os.path.isfile(filepath):
        return False
    if not filepath.endswith(".{}".format(ext)):
        return False
    return True


def select_filepath_open(root, ext):
    """Select a filepath for opening a session.

    Parameters
    ----------
    root : str
        Base directory from where the file selection is started.
        If no directory is provided, the parent folder of the current
        Rhino document will be used
    ext : str
        The type of file that can be openend.

    Returns
    -------
    tuple
        The parent directory.
        The file name.
    None
        If the procedure fails.

    Notes
    -----
    The file extension is only used to identify the type of session file.
    Regardless of the provided extension, the file contents should be in JSON format.

    """
    ext = ext.split('.')[-1]

    if not root:
        root = HERE

    filepath = compas_rhino.select_file(folder=root, filter=ext)

    if not is_session_file(filepath, ext):
        print("This is not a valid session file: {}".format(filepath))
        return

    return filepath


def select_filepath_save(root, ext):
    """Select a filepath for saving a session."""
    if not root:
        root = HERE

    dirname = compas_rhino.select_folder(default=root)
    filename = compas_rhino.rs.GetString('File name (w/o extension)')

    if not filename:
        return

    basename = "{}.{}".format(filename, ext)
    filepath = os.path.join(dirname, basename)

    return filepath


config = {
    "name": "file",
    "message": "File",
    "options": [
        {
            "name": "open",
            "message": "Open",
            "action": select_filepath_open
        },
        {
            "name": "save",
            "message": "Save",
            "action": select_filepath_save
        },
        {
            "name": "saveas",
            "message": "Save As",
            "action": select_filepath_save
        }
    ]
}


def RunCommand(is_interactive):
    # can this be moved to a decorator
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    # store the filepath of the opened session
    if action["name"] == "open":
        filepath = action["action"](RV2["session"]["cwd"], RV2["session"]["ext"])
        if not filepath:
            return

        RV2["session"]["current"] = filepath
        RV2["session"]["cwd"] = os.path.dirname(filepath)

        with open(filepath, "r") as f:
            session = json.load(f, cls=DataDecoder)
            settings = session.get("settings")
            data = session.get("data")

        if settings:
            RV2["settings"].update(settings)

        form, force = None, None

        if data:
            formdata = data.get("form")
            forcedata = data.get("force")

            if formdata:
                form = FormDiagram.from_data(formdata)
                rhinoform = RhinoFormDiagram(form)
                rhinoform.draw(RV2["settings"])

                rhinothrust = RhinoThrustDiagram(form)
                rhinothrust.draw(RV2["settings"])

            if forcedata:
                force = ForceDiagram.from_data(forcedata)
                force.primal = form
                rhinoforce = RhinoForceDiagram(force)
                rhinoforce.draw(RV2["settings"])

        RV2["scene"]["form"] = rhinoform
        RV2["scene"]["force"] = rhinoforce
        RV2["scene"]["thrust"] = rhinothrust

    # only ask for a filepath if there is none
    elif action["name"] == "save":
        filepath = RV2["session"]["current"]
        if not filepath:
            filepath = action["action"](RV2["session"]["cwd"], RV2["session"]["ext"])
        if not filepath:
            return

        data = {"session": RV2["session"], "settings": RV2["settings"], "data": {"form": None, "force": None}}

        if RV2["scene"]["form"]:
            data["data"]["form"] = RV2["scene"]["form"].diagram.to_data()

        if RV2["scene"]["force"]:
            data["data"]["force"] = RV2["scene"]["force"].diagram.to_data()

        with open(filepath, 'w+') as f:
            json.dump(data, f, cls=DataEncoder)

    # always ask for a filepath
    elif action["name"] == "saveas":
        filepath = action["action"](RV2["session"]["cwd"], RV2["session"]["ext"])
        if not filepath:
            return

        data = {"session": RV2["session"], "settings": RV2["settings"], "data": {"form": None, "force": None}}

        if RV2["scene"]["form"]:
            data["data"]["form"] = RV2["scene"]["form"].diagram.to_data()

        if RV2["scene"]["force"]:
            data["data"]["force"] = RV2["scene"]["force"].diagram.to_data()

        with open(filepath, 'w+') as f:
            json.dump(data, f, cls=DataEncoder)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
