from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import subprocess
import json
import os
import compas
import compas_rhino
from compas_rhino.uninstall import uninstall

try:
    from compas_bootstrapper import CONDA_EXE
except ImportError:
    CONDA_EXE = 'conda'


def run(cmd):
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=compas._os.prepare_environment())
    stdout, stderr = p.communicate()
    return stdout, stderr, p.returncode


def install_env_packages(env_name, envs=None, packages=None):

    envs = envs or list_envs(show_packages=False)
    for env in envs:
        name = os.path.split(env)[-1]
        if name == env_name:
            env_path = env
            python_path = os.path.join(env_path, 'python.exe')
            if not os.path.isfile(python_path):
                python_path = os.path.join(env_path, 'bin', 'python')

            if packages:
                to_install = packages
            else:
                packages = packages or list_package(env_name)
                to_install = []
                for p in packages:
                    if p['name'].find('compas') == 0:
                        to_install.append(p['name'].replace('-', '_'))

            print(to_install)

            to_install = ' '.join(to_install)
            cmd = '%s -m compas_rhino.install -p %s' % (python_path, to_install)
            print(cmd)
            out, err, code = run(cmd)
            if code == 0:
                print(out.decode())
                print("Installation finished! Please restart rhino for changes to take effect!")
            else:
                print('exit with code', code)
                print(err.decode())

            return

    print('environment not found!')


def list_package(name):
    out, err, code = run('%s list -n %s --json' % (CONDA_EXE, name))
    packages = json.loads(out.decode())
    return packages


def list_envs(show_packages=True):
    out, err, code = run('%s env list --json' % CONDA_EXE)
    if code == 0:
        envs = json.loads(out.decode())
        for env in envs['envs']:
            if env.find('envs') < 0:
                name = 'base'
            else:
                name = os.path.split(env)[-1]
            print(name)
            if show_packages:
                packages = list_package(name)
                for p in packages:
                    if p['name'].find('compas') == 0:
                        print('    %s:%s  %s' % (p['name'], p['version'], p['channel']))
            print('-'*20)

        return envs['envs']

    else:
        print('exit with code', code)
        print(err.decode())


def RunCommand(is_interactive):
    # TODO: detect version
    ipylib_path = compas_rhino._get_ironpython_lib_path("6.0")
    print(ipylib_path)
    compas_packages = [(name, False) for name in os.listdir(ipylib_path) if name.split("_")[0] =="compas" and name != "compas_bootstrapper.py"]
    results = rs.CheckListBox(compas_packages, "Select Packages to uninstall")

    if results:
        uninstall(results)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
