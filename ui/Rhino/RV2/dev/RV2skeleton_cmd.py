from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc
import rhinoscriptsyntax as rs
# from System.Windows.Forms import Cursor, Cursors

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rhino.etoforms import TextForm
from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import RhinoSkeleton
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


def create(root):
    guids = compas_rhino.select_lines()
    if not guids:
        return
    lines = compas_rhino.get_line_coordinates(guids)
    skeleton = Skeleton.from_skeleton_lines(lines)
    rs.DeleteObjects(guids)
    rhinoskeleton = RhinoSkeleton(skeleton)
    rhinoskeleton.draw_skeleton_branches()
    rhinoskeleton.dynamic_draw_self()

    return rhinoskeleton.diagram


def modify(root):
    RV2 = sc.sticky["RV2"]
    skeleton = RV2["scene"]["skeleton"]
    rhinoskeleton = RhinoSkeleton(skeleton)

    config = {
        "name": "modify",
        "message": "Modify",
        "options": [
            {
                "name": "finish",
                "message": "Finish",
                "action": None
            },
            {
                "name": "move_skeleton",
                "message": "Move_Skeleton",
                "action": rhinoskeleton.move_skeleton_vertex
            },
            {
                "name": "move_vertex",
                "message": "Move_Vertex",
                "action": rhinoskeleton.move_diagram_vertex
            },
            {
                "name": "node_width",
                "message": "Node_Width",
                "action": rhinoskeleton.dynamic_draw
            },
            {
                "name": "leaf_width",
                "message": "Leaf_Width",
                "action": rhinoskeleton.dynamic_draw
            },
            {
                "name": "add_lines",
                "message": "Add_Lines",
                "action": rhinoskeleton.add_lines
            },
            {
                "name": "remove_lines",
                "message": "Remove_Lines",
                "action": rhinoskeleton.remove_lines
            },
            {
                "name": "subdivide",
                "message": "Subdivide",
                "action": rhinoskeleton.diagram.subdivide
            },
            {
                "name": "merge",
                "message": "Merge",
                "action": rhinoskeleton.diagram.merge
            }
        ]
    }

    while True:
        menu = CommandMenu(config)
        action = menu.select_action()
        if not action:
            return

        elif action['name'] == 'leaf_width':
            if rhinoskeleton.diagram.skeleton_vertices()[1] != []:
                action['action']('leaf_width')
            else:
                print('this skeleton doesn\'t have any leaf!')
        elif action['name'] == 'node_width':
            action['action']('node_width')

        elif action['name'] == 'finish':
            break
        else:
            action['action']()
        rhinoskeleton.draw_self()

    skeleton = rhinoskeleton.diagram
    return skeleton


def to_diagram(root):
    RV2 = sc.sticky["RV2"]
    skeleton = RV2["scene"]["skeleton"]
    diagram = skeleton.to_diagram()

    return diagram


config = {
    "name": "skeleton",
    "message": "Skeleton",
    "options": [
        {
            "name": "create",
            "message": "Create",
            "action": create
        },
        {
            "name": "modify",
            "message": "Modify",
            "action": modify
        },
        {
            "name": "to_diagram",
            "message": "To_Diagram",
            "action": to_diagram
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
    scene = RV2["scene"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    if action['name'] != 'to_diagram':

        skeleton = action['action'](session["cwd"])

        if not skeleton:
            return

        rhinoskeleton = RhinoSkeleton(skeleton)
        rhinoskeleton.draw_self()

        scene["skeleton"] = skeleton

    else:
        form = action['action'](session["cwd"])
        if not form:
            return

        rhinoform = RhinoFormDiagram(form)
        rhinoform.draw(settings)

        scene["form"] = rhinoform

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
