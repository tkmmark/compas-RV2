from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import scriptcontext as sc

import compas_rhino
from compas_rhino.etoforms import TextForm
from compas_rhino.ui import CommandMenu


__commandname__ = "RV2form_select"


HERE = compas_rhino.get_document_dirname()


def match_vertices(diagram, keys):
    temp = compas_rhino.get_objects(name="{}.vertex.*".format(diagram.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')
        key = literal_eval(parts[2])
        if key in keys:
            guids.append(guid)
    return guids


def match_edges(diagram, keys):
    temp = compas_rhino.get_objects(name="{}.edge.*".format(diagram.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')[2].split('-')
        u = literal_eval(parts[0])
        v = literal_eval(parts[1])
        if (u, v) in keys or (v, u) in keys:
            guids.append(guid)
    return guids


def match_faces(diagram, keys):
    temp = compas_rhino.get_objects(name="{}.face.*".format(diagram.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')
        key = literal_eval(parts[2])
        if key in keys:
            guids.append(guid)
    return guids


def select_vertices(diagram, keys):
    guids = match_vertices(diagram, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_edges(diagram, keys):
    guids = match_edges(diagram, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_faces(diagram, keys):
    guids = match_faces(diagram, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_boundary_vertices(diagram):
    vertices = diagram.vertices_on_boundary()
    select_vertices(diagram, vertices)


def select_continuous_vertices(diagram):
    edges = diagram.select_edges()
    vertices = []
    for edge in edges:
        continuous = diagram.continuous_vertices(edge)
        vertices.extend(continuous)
    select_vertices(diagram, vertices)


def select_boundary_edges(diagram):
    edges = diagram.edges_on_boundary()
    select_edges(diagram, edges)


def select_continuous_edges(diagram):
    selected = diagram.select_edges()
    edges = []
    for edge in selected:
        continuous = diagram.continuous_edges(edge)
        edges.extend(continuous)
    select_edges(diagram, edges)


def select_parallel_edges(diagram):
    selected = diagram.select_edges()
    edges = []
    for edge in selected:
        parallel = diagram.parallel_edges(edge)
        edges.extend(parallel)
    select_edges(diagram, edges)


def select_boundary_faces(diagram):
    faces = diagram.faces_on_boundary()
    select_faces(diagram, faces)


def select_parallel_faces(diagram):
    selected = diagram.select_edges()
    faces = []
    for edge in selected:
        parallel = diagram.parallel_faces(edge)
        faces.extend(parallel)
    select_faces(diagram, faces)


config = {
    "message": "FormDiagram Select",
    "options": [
        {"name": "Vertices", "message": "Select Vertices", "options": [
            {"name": "Boundary", "action": select_boundary_vertices},
            {"name": "Continuous", "action": select_continuous_vertices}
        ]},
        {"name": "Edges", "message": "Select Edges", "options": [
            {"name": "Boundary", "action": select_boundary_edges},
            {"name": "Continuous", "action": select_continuous_edges},
            {"name": "Parallel", "action": select_parallel_edges}
        ]},
        {"name": "Faces", "message": "Select Faces", "options": [
            {"name": "Boundary", "action": select_boundary_faces},
            {"name": "Parallel", "action": select_parallel_faces}
        ]}
    ]
}


def RunCommand(is_interactive):
    if "RV2" not in sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return

    RV2 = sc.sticky["RV2"]
    rhinoform = RV2["scene"]["form"]

    if not rhinoform:
        return

    settings = RV2["settings"]

    menu = CommandMenu(config)
    action = menu.select_action()

    if not action:
        return

    if action["action"](rhinoform):
        rhinoform.draw(settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
