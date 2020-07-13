from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
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
        selected = rs.ListBox(options, "Select env to install")
        if selected:
            packages = list_package(selected)
            options = []
            for p in packages:
                if p['name'].find('compas') == 0:
                    entry = "%s   %s   %s" % (p['name'].replace('-', '_'), p['version'], p['channel'])
                    options.append((entry, False))

            if options:
                results = rs.CheckListBox(options, "Install compas packages to install from [%s]:" % selected)
                if results:
                    to_install = []
                    for package, yes in results:
                        if yes:
                            name = package.split("   ")[0]
                            to_install.append(name)
                    install_env_packages(selected, envs=envs, packages=to_install)

            else:
                print("no compas package found in env: %s" % selected)
# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
