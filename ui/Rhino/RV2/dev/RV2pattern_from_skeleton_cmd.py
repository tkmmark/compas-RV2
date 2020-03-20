from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import Skeleton
from compas_rv2.rhino import SkeletonObject


__commandname__ = "RV2pattern_from_skeleton"


HERE = compas_rhino.get_document_dirname()


def skeleton_move_skeleton_vertex(skeletonobject):
    skeletonobject.move_skeleton_vertex()


def skeleton_move_diagram_vertex(skeletonobject):
    skeletonobject.move_diagram_vertex()


def skeleton_dynamic_draw_nodewidth(skeletonobject):
    skeletonobject.dynamic_draw('node_width')


def skeleton_dynamic_draw_leafwidth(skeletonobject):
    if skeletonobject.datastructure.skeleton_vertices()[1] != []:
        skeletonobject.dynamic_draw('leaf_width')
    else:
        print("This skeleton doesn't have leaf vertices!")


def skeleton_add_lines(skeletonobject):
    skeletonobject.add_lines()


def skeleton_remove_lines(skeletonobject):
    skeletonobject.remove_lines()


def skeleton_subdivide(skeletonobject):
    skeletonobject.datastructure.subdivide()


def skeleton_merge(skeletonobject):
    skeletonobject.datastructure.merge()


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

    # skeleton from lines
    guids = compas_rhino.select_lines()
    if not guids:
        return

    lines = compas_rhino.get_line_coordinates(guids)
    skeleton = Skeleton.from_skeleton_lines(lines)
    if not skeleton:
        return

    compas_rhino.delete_objects(guids)

    # pattern from skeleton / skeleton to pattern
    skeletonobject = SkeletonObject(skeleton)
    skeletonobject.draw_skeleton_branches()
    skeletonobject.dynamic_draw_self()

    # modify skeleton
    while True:
        menu = CommandMenu(config)
        action = menu.select_action()
        if not action:
            return

        if action['name'] == 'finish':
            break

        action['action'](skeletonobject)
        skeletonobject.draw_self()

    # make pattern
    pattern = skeletonobject.datastructure.to_pattern()

    # clear skeleton
    compas_rhino.clear_layer('Skeleton')

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
