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


__commandname__ = "RV2init"


SETTINGS = {

    "rv2": {
        "section1.bool.example": False,
        "section2.num.example": 1.0,
    },

    "solver": {
        "tna.vertical.kmax": 300,
        "tna.vertical.zmax": 4.0,
        "tna.horizontal.kmax": 100,
        "tna.horizontal.alpha": 100,
    }

}


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME


def RunCommand(is_interactive):

    Browser()

    errorHandler = ErrorHandler(title="Server side Error", showLocalTraceback=False)
    sc.sticky["RV2.proxy"] = Proxy(errorHandler=errorHandler)

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
