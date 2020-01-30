from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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
    from compas_rhino.forms import BrowserForm


__commandname__ = "RV2init"


def RunCommand(is_interactive):
    p = Proxy()

    sc.sticky["RV2.proxy"] = p

    sc.sticky["RV2"] = {
        "session": {
            "cwd": None,
            "ext": 'rv2',
            "current": None
        },

        "scene": {
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
            "show.form.faces": False,

            "show.force.vertices": True,
            "show.force.edges": True,
            "show.force.faces": False,

            "show.thrust.vertices": True,
            "show.thrust.edges": True,
            "show.thrust.faces": True,

            "color.form.vertices": (0, 255, 0),
            "color.form.vertices:is_fixed": (0, 255, 255),
            "color.form.vertices:is_external": (0, 0, 255),
            "color.form.vertices:is_anchor": (255, 0, 0),

            "color.form.edges": (0, 255, 0),
            "color.form.edges:is_external": (0, 0, 255),

            "color.thrust.vertices": (255, 0, 255),
            "color.thrust.vertices:is_fixed": (0, 255, 0),
            "color.thrust.vertices:is_anchor": (255, 0, 0),

            "color.thrust.edges": (255, 0, 255),
            "color.thrust.faces": (255, 0, 255),

            "color.force.vertices": (0, 255, 0),
            "color.force.vertices:is_fixed": (0, 255, 255),

            "color.force.edges": (0, 255, 0),
            "color.force.edges:is_external": (0, 0, 255),

            "vertical.zmax": 4.0,
            "vertical.kmax": 100,

            "horizontal.kmax": 100,
            "horizontal.alpha": 100
        }
    }

    settings = sc.sticky["RV2"]["settings"]
    layers = [settings[name] for name in settings if name.startswith("layers")]
    compas_rhino.clear_layers(layers)

    browser = BrowserForm('https://compas-dev.github.io/main/', width=960, height=720)
    browser.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
