from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import importlib
import subprocess
import os
import sys
import rhinoscriptsyntax as rs
import tarfile

__commandname__ = "RV2install"

def RunCommand(is_interactive):
    packages = ['compas', 'compas_rhino', 'compas_ags', 'compas_tna','compas_pattern']

    print('Installed Modules:')
    for p in packages:
        try:
            module = importlib.import_module(p)
            if hasattr(module,'__version__'):
                print(p,module.__version__)
            else:
                print(p, 'no version info')
        except ImportError:
            module = None
            print(p, 'Not found')

    RV2_path = os.path.dirname(os.path.dirname(__file__))

    # env_tar_gz = os.path.join(RV2_path, 'env.tar.gz')
    # env_path = os.path.join(RV2_path, 'env')
    # if os.path.exists(env_tar_gz):
    #     print('unzip compas library:')
    #     tar = tarfile.open(env_tar_gz, "r:gz")
    #     tar.extractall(env_path)
    #     tar.close()


    python_path = os.path.join(RV2_path,'env','bin','python')
    p = subprocess.Popen([python_path, '-m', 'compas_rhino.install','-p'] + packages, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    
    print('start installing')
    print(stdout)
    print(stderr)
    rs.MessageBox("Install finished Please restart")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
