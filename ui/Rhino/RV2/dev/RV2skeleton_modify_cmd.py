from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import get_scene


__commandname__ = "RV2skeleton_modify"


HERE = compas_rhino.get_document_dirname()


def skeleton_move_skeleton_vertex(rhinoskeleton):
    rhinoskeleton.move_skeleton_vertex()


def skeleton_move_diagram_vertex(rhinoskeleton):
    rhinoskeleton.move_diagram_vertex()


def skeleton_dynamic_draw_nodewidth(rhinoskeleton):
    rhinoskeleton.dynamic_draw('node_width')


def skeleton_dynamic_draw_leafwidth(rhinoskeleton):
    if rhinoskeleton.diagram.skeleton_vertices()[1] != []:
        rhinoskeleton.dynamic_draw('leaf_width')
    else:
        print("This skeleton doesn't have leaf vertices!")


def skeleton_add_lines(rhinoskeleton):
    rhinoskeleton.add_lines()


def skeleton_remove_lines(rhinoskeleton):
    rhinoskeleton.remove_lines()


def skeleton_subdivide(rhinoskeleton):
    rhinoskeleton.diagram.subdivide()


def skeleton_merge(rhinoskeleton):
    rhinoskeleton.diagram.merge()


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
            "action": skeleton_move_skeleton_vertex
        },
        {
            "name": "move_vertex",
            "message": "Move_Vertex",
            "action": skeleton_move_diagram_vertex
        },
        {
            "name": "node_width",
            "message": "Node_Width",
            "action": skeleton_dynamic_draw_nodewidth
        },
        {
            "name": "leaf_width",
            "message": "Leaf_Width",
            "action": skeleton_dynamic_draw_leafwidth
        },
        {
            "name": "add_lines",
            "message": "Add_Lines",
            "action": skeleton_add_lines
        },
        {
            "name": "remove_lines",
            "message": "Remove_Lines",
            "action": skeleton_remove_lines
        },
        {
            "name": "subdivide",
            "message": "Subdivide",
            "action": skeleton_subdivide
        },
        {
            "name": "merge",
            "message": "Merge",
            "action": skeleton_merge
        }
    ]
}


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    rhinoskeleton = scene.get('skeleton')

    if not rhinoskeleton:
        return

    while True:
        menu = CommandMenu(config)
        action = menu.select_action()
        if not action:
            return

        if action['name'] == 'finish':
            break

        # rename this to 'handler'
        action['action'](rhinoskeleton)
        rhinoskeleton.draw_self()

    # rhinoskeleton.draw_self()
    # scene["skeleton"] = rhinoskeleton


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
