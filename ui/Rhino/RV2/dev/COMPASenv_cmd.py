from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import subprocess
import json
import os

try:
    from compas_bootstrapper import CONDA_EXE
except ImportError:
    CONDA_EXE = 'conda'


def run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout, stderr, p.returncode


def install_env_packages(env_path, packages):
    python_path = os.path.join(env_path, 'python')
    if not os.path.isfile(python_path):
        python_path = os.path.join(env_path, 'bin', 'python')

    packages = ' '.join(packages)
    out, err, code = run('%s -m compas_rhino.install -p %s' % (python_path, packages))
    if code == 0:
        print(out.decode())
    else:
        print('exit with code', code)
        print(err.decode())


def list_all():
    out, err, code = run('%s env list --json' % CONDA_EXE)

    if code == 0:
        envs = json.loads(out.decode())
        for env in envs['envs']:
            if env.find('envs') < 0:
                name = 'base'
            else:
                name = os.path.split(env)[-1]
            print(name)

            out, err, code = run('%s list -n %s --json' % (CONDA_EXE, name))
            packages = json.loads(out.decode())
            for p in packages:
                if p['name'].find('compas') == 0:
                    print('    %s:%s  %s' % (p['name'], p['version'], p['channel']))
            print('-'*20)

    else:
        print('exit with code', code)
        print(err.decode())


def RunCommand(is_interactive):
    list_all()
    # install_env_packages('/Users/lichen7/anaconda3/envs/rv2',['compas','compas_rv2'])

    # import compas
    # env = compas._os.prepare_environment()
    # # print(env['PATH'])
    # # env['PATH']+= ':/Users/lichen7/anaconda3/bin'

    # p = subprocess.Popen(["conda"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # stdout,stderr = p.communicate()
    # print(stdout.decode())
    # print(stderr.decode())

# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    RunCommand(True)
