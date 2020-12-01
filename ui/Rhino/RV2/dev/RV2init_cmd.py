from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc

import compas_rhino

from compas_cloud import Proxy  # noqa: E402
from compas_rv2.web import Browser  # noqa: E402
from compas_rv2.scene import Scene  # noqa: E402
from compas_rv2.rhino import ErrorHandler  # noqa: E402
from compas_rv2.activate import check
from compas_rv2.activate import activate

__commandname__ = "RV2init"


SETTINGS = {

    "RV2": {
        "show.forces": False,
        "show.angles": True,
        "tol.angles": 5.0
    },

    "Solvers": {
        "tna.vertical.kmax": 300,
        "tna.vertical.zmax": 4.0,
        "tna.horizontal.kmax": 100,
        "tna.horizontal.alpha": 100,
        "tna.horizontal.refreshrate": 10,
    }

}


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME


def RunCommand(is_interactive):

    if check():
        print("Current plugin is already activated")
    else:
        compas_rhino.rs.MessageBox("Env has changed, re-activating plugin", 0, "Re-activating Needed")
        if activate():
            compas_rhino.rs.MessageBox("Restart Rhino for the change to take effect", 0, "Restart Rhino")
        else:
            compas_rhino.rs.MessageBox("Someting wrong during re-activation", 0, "Error")
        return

    Browser()

    errorHandler = ErrorHandler(title="Server side Error", showLocalTraceback=False)
    sc.sticky["RV2.proxy"] = Proxy(errorHandler=errorHandler)
    sc.sticky["RV2.proxy"].restart()

    sc.sticky["RV2.system"] = {
        "session.dirname": CWD,
        "session.filename": None,
        "session.extension": 'rv2'
    }

    scene = Scene(SETTINGS)
    scene.clear()

    sc.sticky["RV2"] = {"scene": scene}

    sc.sticky["RV2.sessions"] = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
