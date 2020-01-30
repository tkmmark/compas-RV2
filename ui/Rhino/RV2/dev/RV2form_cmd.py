from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc
import rhinoscriptsyntax as rs

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rhino.etoforms import TextForm
from compas_rv2.datastructures import FormDiagram
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
    guids = compas_rhino.select_lines()
    if not guids:
        return
    lines = compas_rhino.get_line_coordinates(guids)
    skeleton = Skeleton.from_skeleton_lines(lines)
    rs.DeleteObjects(guids)
    rhinoskeleton = RhinoSkeleton(skeleton)
    rhinoskeleton.dynamic_draw_self()

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
            rs.PurgeLayer('skeleton_vertices')
            rs.PurgeLayer('skeleton_diagram_vertices')
            rs.PurgeLayer('skeleton_edges')
            rs.PurgeLayer('skeleton_diagram_edges')
            break
        else:
            action['action']()
        rhinoskeleton.draw_self()

    form = rhinoskeleton.diagram.to_diagram()
    # keys = rhinoskeleton.diagram.to_support_vertices()

    # if keys:
    #     form.vertices_attributes(['is_anchor', 'is_fixed'], [True, True], keys=keys)
    # form.update_boundaries(feet=2)

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
