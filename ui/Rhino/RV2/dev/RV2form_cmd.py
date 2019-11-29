from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rhino.etoforms import TextForm
from compas_rv2.diagrams import FormDiagram
from compas_rv2.rhino import RhinoFormDiagram


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
        }
     ]
}


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]

    session = RV2["session"]
    settings = RV2["settings"]
    data = RV2["data"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    form = action['action'](session["cwd"])

    if not form:
        return

    diagram = RhinoFormDiagram(form)
    diagram.draw(settings)

    data["form"] = form


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
