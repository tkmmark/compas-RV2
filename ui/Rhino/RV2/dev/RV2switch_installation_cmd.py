from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import scriptcontext as sc
import subprocess
import json
import os
import compas

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

            if show_packages:
                print(name)
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

    register_json_path = os.path.join(compas.APPDATA, "compas_plugins.json")
    register_json = json.load(open(register_json_path))

    selected = rs.ListBox(["Releases", "Dev(conda)"], "Select which source to install")

    if selected == "Releases":

        plugins = [path for path in register_json["Plugins"] if os.path.exists(path)]
        location = rs.ListBox(plugins, "Select from which location to install")
        if location:
            # TODO: make this work on mac
            python_path = os.path.join(location, "dev", "env", "python.exe")
            cmd = "%s -m compas_rv2.install --plugin_path %s" % (python_path, location)
            print(cmd)
            stdout, stderr, returncode = run(cmd)
            if returncode == 0:
                print(stdout)
                if "RV2.proxy" in sc.sticky:
                    sc.sticky["RV2.proxy"].shutdown()
                rs.MessageBox("Please restart Rhino to take effect", 0, "Installation Succeed")
            else:
                print(stdout)
                print(stderr)
                rs.MessageBox(stderr, 0, "Installation Failed")

    elif selected == "Dev(conda)":

        print('fetching conda envs....')

        envs = list_envs(show_packages=False)
        envs_dict = {}
        for env_path in envs:
            if env_path.find('envs') < 0:
                name = 'base'
            else:
                name = os.path.split(env_path)[-1]
            envs_dict[name] = env_path
        options = envs_dict.keys()

        if options:
            selected = rs.ListBox(options, "Select conda env to install")
            if selected:
                env_path = envs_dict[selected]
                python_path = os.path.join(env_path, 'python.exe')
                if not os.path.isfile(python_path):
                    python_path = os.path.join(env_path, 'bin', 'python')
                print(python_path)
                cmd = '%s -m compas_rv2.install --dev' % (python_path)
                stdout, stderr, returncode = run(cmd)
                if returncode == 0:
                    print(stdout)
                    if "RV2.proxy" in sc.sticky:
                        sc.sticky["RV2.proxy"].shutdown()
                    rs.MessageBox("Please restart Rhino to take effect", 0, "Installation Succeed")
                else:
                    print(stdout)
                    print(stderr)
                    rs.MessageBox(stderr, 0, "Installation Failed")


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    RunCommand(True)
