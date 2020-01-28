from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# check if the following exist
# - conda: ask user to install Anaconda/Miniconda

# insert local lib in path
# remove again after imports?

# start a proxy with the environment set to use the local libs?

import scriptcontext as sc

try:
    import compas        # noqa: F401
    import compas_rhino  # noqa: F401
    import compas_ags    # noqa: F401
    import compas_tna    # noqa: F401
    import compas_cloud  # noqa: F401

except ImportError:
    # do something here to fix the problem
    raise

else:
    # replace this by from compas_cloud import Proxy
    from compas.rpc import Proxy
    from compas_rhino.etoforms import ImageForm


__commandname__ = "RV2init"


# recode this in a C# plugin
# start the server
# load the plugin toolbar
# restart the server
# ...


def RunCommand(is_interactive):
    p = Proxy()

    sc.sticky["RV2.proxy"] = p

    sc.sticky["RV2"] = {
        "session": {
            "cwd": None,
            "ext": 'rv2',
            "current": None
        },

        "data": {
            "form": None,
            "force": None,
            "thrust": None
        },

        "settings": {
            "layers.form": "RV2::FormDiagram",
            "layers.force": "RV2::ForceDiagram",
            "layers.thrust": "RV2::ThrustNetwork",

            "show.form.vertices": True,
            "show.form.edges": True,
            "show.form.faces": True,

            "show.force.vertices": True,
            "show.force.edges": True,
            "show.force.faces": True,

            "color.form.vertices": (0, 0, 0),
            "color.form.vertices:is_fixed": (0, 255, 0),
            "color.form.vertices:is_external": (0, 0, 255),
            "color.form.vertices:is_anchor": (255, 0, 0),

            "color.form.edges": (0, 0, 0),
            "color.form.faces": (0, 0, 0),

            "vertical.zmax": 4.0,
            "vertical.kmax": 100,

            "horizontal.kmax": 100,
            "horizontal.alpha": 100
        }
        # solver settings?
    }

    # display the "welcome" screen
    form = ImageForm('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')
    form.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
