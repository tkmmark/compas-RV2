from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import Skeleton
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import SkeletonObject


__commandname__ = "RV2pattern_from_skeleton"


def skeleton_move_skeleton_vertex(skeletonobject):
    skeletonobject.move_skeleton_vertex()


def skeleton_move_mesh_vertex(skeletonobject):
    skeletonobject.draw_coarse_mesh_vertices()
    skeletonobject.move_mesh_vertex()
    skeletonobject.clear_coarse_mesh_vertices()


def skeleton_dynamic_draw_nodewidth(skeletonobject):
    skeletonobject.dynamic_update_width('node_width')


def skeleton_dynamic_draw_leafwidth(skeletonobject):
    if skeletonobject.datastructure.skeleton_vertices():
        skeletonobject.dynamic_update_width('leaf_width')
    else:
        print("This skeleton doesn't have leaf vertices!")


def skeleton_dynamic_draw_leafextend(skeletonobject):
    if skeletonobject.datastructure.skeleton_vertices():
        skeletonobject.dynamic_update_width('leaf_extend')
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
            "name": "move_skeleton_vertices",
            "message": "Move_Skeleton_Vertices",
            "action": skeleton_move_skeleton_vertex
        },
        {
            "name": "move_coarse_mesh_corner_vertices",
            "message": "Move_Coarse_Mesh_Corner_Vertices",
            "action": skeleton_move_mesh_vertex
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
            "name": "leaf_extend",
            "message": "Leaf_Extend",
            "action": skeleton_dynamic_draw_leafextend
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
    compas_rhino.rs.HideObjects(guids)
    skeleton = Skeleton.from_skeleton_lines(lines)
    if not skeleton:
        return

    skeletonobject = SkeletonObject(skeleton)
    skeletonobject.draw()
    skeletonobject.dynamic_update_mesh()

    # modify skeleton
    while True:
        menu = CommandMenu(config)
        action = menu.select_action()
        if not action:
            return

        if action['name'] == 'finish':
            break

        action['action'](skeletonobject)
        skeletonobject.draw()

    # make pattern
    mesh = skeletonobject.datastructure.to_mesh()
    xyz = mesh.vertices_attributes('xyz')
    faces = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
    pattern = Pattern.from_vertices_and_faces(xyz, faces)

    # clear skeleton
    skeletonobject.clear()
    compas_rhino.delete_layers([
        skeletonobject.settings['skeleton.layer'],
        skeletonobject.settings['mesh.layer']
        ])

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()

    print('Pattern object successfully created.')

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
