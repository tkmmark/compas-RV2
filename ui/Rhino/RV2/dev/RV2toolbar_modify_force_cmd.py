from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

import RV2force_attributes_cmd
import RV2force_modify_vertices_cmd
import RV2force_modify_edges_cmd
import RV2force_move_vertices_cmd

__commandname__ = "RV2toolbar_modify_force"


def RunCommand(is_interactive):

    options = ["DiagramAttributes", "VerticesAttributes", "EdgesAttributes", "MoveVertices"]
    option = compas_rhino.rs.GetString("Modify force Diagram:", strings=options)

    if not option:
        return

    elif option == "DiagramAttributes":
        RV2force_attributes_cmd.RunCommand(True)

    elif option == "VerticesAttributes":
        RV2force_modify_vertices_cmd.RunCommand(True)

    elif option == "EdgesAttributes":
        RV2force_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV2force_move_vertices_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
