from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc

try:
    import compas        # noqa: F401
    import compas_rhino  # noqa: F401
    import compas_cloud  # noqa: F401
    import compas_ags    # noqa: F401
    import compas_tna    # noqa: F401
    import compas_rv2    # noqa: F401

except ImportError:
    # do something here to fix the problem
    raise

else:
    from compas_cloud import Proxy
    from compas_rv2.web import Browser
    from compas_rv2.scene import Scene


__commandname__ = "RV2init"


SETTINGS = {
    'pattern.show.vertices': True,
    'pattern.show.edges': True,
    'pattern.show.faces': True,
    'pattern.show.faces:joined': False,
    'pattern.color.vertices': [255, 255, 255],
    'pattern.color.vertices:is_anchor': [255, 0, 0],
    'pattern.color.vertices:is_fixed': [0, 0, 255],
    'pattern.color.edges': [0, 0, 0],
    'pattern.color.faces': [200, 200, 200],
    'pattern.layer': "RV2::Pattern",

    'form.show.vertices': True,
    'form.show.edges': True,
    'form.show.faces': False,
    'form.color.vertices': [0, 255, 0],
    'form.color.vertices:is_fixed': [0, 255, 255],
    'form.color.vertices:is_external': [0, 0, 255],
    'form.color.vertices:is_anchor': [255, 255, 255],
    'form.color.edges': [0, 255, 0],
    'form.color.edges:is_external': [0, 0, 255],
    'form.layer': "RV2::FormDiagram",

    'force.show.vertices': True,
    'force.show.edges': True,
    'force.show.faces': False,
    'force.color.vertices': [0, 255, 0],
    'force.color.vertices:is_fixed': [0, 255, 255],
    'force.color.edges': [0, 255, 0],
    'force.color.edges:is_external': [0, 0, 255],
    'force.layer': "RV2::ForceDiagram",

    'thrust.show.vertices': True,
    'thrust.show.edges': True,
    'thrust.show.faces': True,
    'thrust.color.vertices': [255, 0, 255],
    'thrust.color.vertices:is_fixed': [0, 255, 0],
    'thrust.color.vertices:is_anchor': [255, 0, 0],
    'thrust.color.edges': [255, 0, 255],
    'thrust.color.faces': [255, 0, 255],
    'thrust.scale.external': 0.1,
    'thrust.layer': "RV2::ThrustDiagram",

    "tna.vertical.kmax": 100,
    "tna.vertical.zmax": 4.0,
    "tna.horizontal.kmax": 100,
    "tna.horizontal.alpha": 100,
}


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME


def RunCommand(is_interactive):

    # RV2.system
    # RV2.settings
    # RV2.proxy
    # RV2.data
    # RV2.scene

    # perhaps we should make this specificly about a "splash" window
    Browser()

    sc.sticky["RV2.proxy"] = Proxy()

    # how to update this when Rhino file is saved?
    sc.sticky["RV2.system"] = {
        "session.dirname": CWD,
        "session.filename": None,
        "session.extension": 'rv2'
    }

    # perhaps it would make sense to make the secene configurable
    # and to allow this configuration to be changed explicitly by the user
    scene = Scene(SETTINGS)
    scene.clear()

    sc.sticky["RV2"] = {
        "scene": scene,
    }


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
