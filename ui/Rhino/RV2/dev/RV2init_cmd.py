from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc

try:
    import compas        # noqa: F401
    import compas_rhino  # noqa: F401
    import compas_cloud  # noqa: F401
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
    "tna.vertical.kmax": 300,
    "tna.vertical.zmax": 4.0,
    "tna.horizontal.kmax": 100,
    "tna.horizontal.alpha": 100,
}


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME


def RunCommand(is_interactive):

    Browser()

    sc.sticky["RV2.proxy"] = Proxy()

    sc.sticky["RV2.system"] = {
        "session.dirname": CWD,
        "session.filename": None,
        "session.extension": 'rv2'
    }

    scene = Scene(SETTINGS)
    scene.clear()

    sc.sticky["RV2"] = {"scene": scene}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
