import os
import subprocess
import sys
from shutil import copyfile
import pkg_resources

branch = None

WEBAPP_PATH = "./static/org.geppetto.frontend/src/main/webapp/"
DEPENDENCIES_PATH = './dependencies/'
JUPYTER_EXTENSION_PATH = DEPENDENCIES_PATH+'org.geppetto.frontend.jupyter/'
PYGEPPETTO_PATH = DEPENDENCIES_PATH + 'pygeppetto/'
PYNWB_PATH = DEPENDENCIES_PATH + 'pynwb/'

# by default clones branch (which can be passed as a parameter python install.py branch test_branch)
# if branch doesnt exist clones the default_branch


def clone(repository, folder, default_branch, cwdp='', recursive=False, destination_folder=None):
    global branch
    print("Cloning " + repository)
    if recursive:
        subprocess.call(['git', 'clone', '--recursive',
                         repository], cwd='./' + cwdp)
    else:
        if destination_folder:
            subprocess.call(['git', 'clone', repository,
                             destination_folder], cwd='./' + cwdp)
        else:
            subprocess.call(['git', 'clone', repository], cwd='./' + cwdp)
    checkout(folder, default_branch, cwdp)


def checkout(folder, default_branch, cwdp):
    currentPath = os.getcwd()
    print(currentPath)
    newPath = currentPath + "/" + cwdp + folder
    print(newPath)
    os.chdir(newPath)
    python_git = subprocess.Popen(
        "git branch -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outstd, errstd = python_git.communicate()
    if branch and branch in str(outstd):
        subprocess.call(['git', 'checkout', branch], cwd='./')
    else:
        subprocess.call(['git', 'checkout', default_branch], cwd='./')
    os.chdir(currentPath)


def main(argv):
    global branch
    if (len(argv) > 0):
        if (argv[0] == 'branch'):
            branch = argv[1]


if __name__ == "__main__":
    main(sys.argv[1:])

os.chdir(os.getcwd() + "/../")
# # Cloning Repos
# clone('https://github.com/openworm/pygeppetto.git', 'pygeppetto', 'development')
subprocess.call(['pip', 'install', '-e', '.'], cwd=PYGEPPETTO_PATH)


subprocess.call(['pip', 'install', '-e', '.'], cwd=PYNWB_PATH)

# clone('https://github.com/openworm/org.geppetto.frontend.jupyter.git', 'org.geppetto.frontend.jupyter', 'refactor-sync')
subprocess.call(['npm', 'install'], cwd=JUPYTER_EXTENSION_PATH+'js')
subprocess.call(['npm', 'run', 'build-dev'], cwd=JUPYTER_EXTENSION_PATH+'js')

# # subprocess.call(['git', 'submodule', 'update', '--init'], cwd='./')
# clone('https://github.com/openworm/org.geppetto.frontend.git', 'geppetto', 'refactor-upgrade-materialui', 'hnn_ui/', False, 'geppetto')
# # checkout('geppetto', 'development','org.geppetto.frontend.jupyter/src/jupyter_geppetto/')
# clone('https://github.com/MetaCell/geppetto-hnn.git', 'geppetto-hnn', 'development',
#       'hnn_ui/geppetto/src/main/webapp/extensions/')


print("Enabling Geppetto Extension ...")
geppetto_configuration = os.path.join(os.path.dirname(
    __file__), './utilities/GeppettoConfiguration.json')
copyfile(geppetto_configuration, WEBAPP_PATH + 'GeppettoConfiguration.json')

# Installing and building
print("NPM Install and build for Geppetto Frontend  ...")
# subprocess.call(['npm', 'install'], cwd=WEBAPP_PATH)
# subprocess.call(['npm', 'run', 'build-dev-noTest'], cwd=WEBAPP_PATH)

print("Installing jupyter_geppetto python package ...")


if 'jupyter_geppetto' not in (pkg.key for pkg in pkg_resources.working_set):
    subprocess.call(['pip', 'install', '-e', '.'], cwd=JUPYTER_EXTENSION_PATH)
else:
    subprocess.call(['pip', 'install', '--upgrade', '--no-deps',
                     '--force-reinstall', '-e', '.'], cwd=JUPYTER_EXTENSION_PATH)


print("Installing jupyter_geppetto Jupyter Extension ...")
subprocess.call(['jupyter', 'nbextension', 'install', '--py', '--symlink', ' --sys-prefix', 'jupyter_geppetto'],
                cwd=JUPYTER_EXTENSION_PATH)
subprocess.call(['jupyter', 'nbextension', 'enable', '--py', ' --sys-prefix', 'jupyter_geppetto'],
                cwd=JUPYTER_EXTENSION_PATH)
subprocess.call(['jupyter', 'nbextension', 'enable', '--py', 'widgetsnbextension'],
                cwd=JUPYTER_EXTENSION_PATH)
subprocess.call(['jupyter', 'serverextension', 'enable', '--py', 'jupyter_geppetto'],
                cwd=JUPYTER_EXTENSION_PATH)

print("Installing UI python package ...")
#subprocess.call(['pip', 'install', '-e', '.'], cwd='.')
