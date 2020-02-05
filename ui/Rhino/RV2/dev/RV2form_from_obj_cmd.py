from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rv2.datastructures import FormDiagram
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoThrustDiagram


__commandname__ = "RV2form_from_obj"


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


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]

    session = RV2["session"]
    settings = RV2["settings"]
    scene = RV2["scene"]

    form = from_obj(session["cwd"])

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
