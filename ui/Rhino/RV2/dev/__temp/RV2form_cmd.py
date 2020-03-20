from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import get_rv2
from compas_rv2.datastructures import FormDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoThrustDiagram


__commandname__ = "RV2form"


HERE = compas_rhino.get_document_dirname()


def is_valid_file(filepath, ext):
    """Is the selected path a valid file.

    Parameters
    ----------
    filepath
    """
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

    if not is_valid_file(filepath, ext):
        print("This is not a valid session file: {}".format(filepath))
        return

    return filepath


def from_obj(root):
    filepath = select_filepath_open(root, 'obj')
    if not filepath:
        return
    form = FormDiagram.from_obj(filepath)
    return form


def from_json(root):
    filepath = select_filepath_open(root, 'json')
    if not filepath:
        return
    form = FormDiagram.from_json(filepath)
    return form


def from_lines(root):
    guids = compas_rhino.select_lines()
    if not guids:
        return
    lines = compas_rhino.get_line_coordinates(guids)
    form = FormDiagram.from_lines(lines)
    return form


def from_mesh(root):
    guid = compas_rhino.select_mesh()
    if not guid:
        return
    form = FormDiagram.from_rhinomesh(guid)
    return form


def from_surface(root):
    # add option for uv versus heighfield?
    # add option for patches?
    guid = compas_rhino.select_surface()
    if not guid:
        return
    form = FormDiagram.from_rhinosurface(guid)
    return form


def from_features(root):
    raise NotImplementedError


def from_skeleton(root):
    RV2 = get_rv2()
    skeleton = RV2["scene"]["skeleton"]
    if not skeleton:
        print('There is not skeleton to be found!')
        return
    form = skeleton.diagram.to_form()
    return form


config = {
    "name": "form",
    "message": "Form",
    "options": [
        {
            "name": "from_obj",
            "message": "From OBJ",
            "action": from_obj
        },
        {
            "name": "from_json",
            "message": "From JSON",
            "action": from_json
        },
        {
            "name": "from_lines",
            "message": "From lines",
            "action": from_lines
        },
        {
            "name": "from_mesh",
            "message": "From mesh",
            "action": from_mesh
        },
        {
            "name": "from_surface",
            "message": "From surface",
            "action": from_surface
        },
        {
            "name": "from_features",
            "message": "From features",
            "action": from_features
        },
        {
            "name": "from_skeleton",
            "message": "From skeleton",
            "action": from_skeleton
        }
     ]
}


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    session = RV2["session"]
    settings = RV2["settings"]
    scene = RV2["scene"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    form = action['action'](session["cwd"])

    if not form:
        return

    rhinoform = RhinoFormDiagram(form)
    rhinoform.draw(settings)

    rhinothrust = RhinoThrustDiagram(form)

    scene["form"] = rhinoform
    scene["force"] = None
    scene["thrust"] = rhinothrust


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
