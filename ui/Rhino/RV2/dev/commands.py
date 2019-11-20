from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino


__all__ = ['open_file', 'save_file', 'saveas_file']


def open_file(RV2):

    if not RV2["settings"]["file.dir"]:
        filepath = compas_rhino.select_file(
            folder=HERE, filter=RV2["settings"]["file.ext"])
    else:
        filepath = compas_rhino.select_file(
            folder=RV2["settings"]["file.dir"], filter=RV2["settings"]["file.ext"])

    if not filepath:
        return

    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)

    RV2["settings"]["file.dir"] = file_dir
    RV2["settings"]["file.name"] = file_name

    if not file_name.endswith(".{}".format(RV2["settings"]["file.ext"])):
        print("The filename is invalid: {}".format(file_name))
        return

    filepath = os.path.join(file_dir, file_name)

    with open(filepath, "r") as f:
        RV2_new = json.load(f)

        form, force, thrust = None, None, None

        if "settings" in RV2_new and RV2_new["settings"]:
            RV2["settings"].update(RV2_new["settings"])

        if "data" in RV2_new and RV2_new["data"]:
            data = RV2_new["data"]
            if "form" in data:
                form = FormDiagram.from_data(data)
                form.draw(RV2["settings"], clear_layer=True)
            if "force" in data:
                force = ForceDiagram.from_data(data)
                force.draw(RV2["settings"], clear_layer=True)
            if "thrust" in data:
                thrust = ThrustDiagram.from_data(data)
                thrust.draw(RV2["settings"], clear_layer=True)

    RV2["data"]["form"] = form
    RV2["data"]["force"] = force
    RV2["data"]["thrust"] = thrust


def save_file(RV2):
    pass


def savesas_file(RV2):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
