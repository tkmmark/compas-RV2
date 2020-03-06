from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.ui import CommandMenu
from compas_rv2.rhino import get_proxy


__commandname__ = "RV2cloud"


def shutdown():
    p = get_proxy()
    p.shutdown()


def restart():

    config = {
        "name": "Cloud",
        "message": "start cloud in ?",
        "options": [
            {
                "name": "background",
                "message": "background",
                "action": None
            },
            {
                "name": "console",
                "message": "console",
                "action": None
            }
        ]
    }

    menu = CommandMenu(config)
    action = menu.select_action()

    if action['name'] == 'background':
        background = True
    if action['name'] == 'console':
        background = False

    p = get_proxy()
    p.background = background
    p.restart()


def check():
    p = get_proxy()
    print(p.check())


def RunCommand(is_interactive):

    config = {
        "name": "Cloud",
        "message": "compad_cloud settings",
        "options": [
            {
                "name": "done",
                "message": "done",
                "action": None
            },
            {
                "name": "shutdown",
                "message": "shutdown",
                "action": shutdown
            },
            {
                "name": "restart",
                "message": "restart",
                "action": restart
            },
            {
                "name": "check",
                "message": "check",
                "action": check
            }
        ]
    }

    while True:
        menu = CommandMenu(config)
        action = menu.select_action()
        if not action:
            return

        if action['name'] == 'done':
            return

        action['action']()


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
