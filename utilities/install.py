import os
import subprocess
import sys
from shutil import copyfile
import pkg_resources

DEFAULT_BRANCHES = ['feature/jupyter-backend', 'feature/extensible_routes', 'development']

WEBAPP_PATH = "./webapp/"
DEPENDENCIES_PATH = './dependencies/'
JUPYTER_EXTENSION_PATH = DEPENDENCIES_PATH+'org.geppetto.frontend.jupyter/'
PYGEPPETTO_PATH = DEPENDENCIES_PATH + 'pygeppetto/'
PYNWB_PATH = DEPENDENCIES_PATH + 'pynwb/'
    # Hack so that it works in python 2 and 3
try:
    input = raw_input
except NameError:
    pass
    
# by default clones branch (which can be passed as a parameter python install.py branch test_branch)
# if branch doesnt exist clones the fallback_branch


def clone(repository, branches, recursive=False, destination_folder=''):
    print("Cloning " + repository)

    if not destination_folder: 
        destination_folder = repository.split('/')[-1][0:-4]

    if recursive:
        subprocess.call(['git', 'clone', '--recursive',
                         repository], cwd='./' )
    else:
        if destination_folder:
            subprocess.call(['git', 'clone', repository,
                             destination_folder], cwd='./')
        else:
            subprocess.call(['git', 'clone', repository], cwd='./')
    checkout(branches, destination_folder)


def checkout(branches, project_root):
    '''
    Checkout the branches in the specified order. The first existing branch is checked out
    '''



    currentPath = os.getcwd()
    # print(currentPath)
    newPath = project_root
    # print(newPath)
    os.chdir(newPath)

    python_git = subprocess.Popen(
        "git branch -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outstd, errstd = python_git.communicate()
    available_branches = str(outstd)

    for branch in branches:
        if branch in available_branches:
            print('Checking out branch', branch)
            subprocess.call(['git', 'checkout', branch], cwd='./')
            break
    else:
        print('No branch has been checked out')
        print('Available branches\n', available_branches)
        branch = input('Choose branch for project {}.\nWrite the branch name and press enter: '.format(project_root.split(os.sep)[-1]))
        subprocess.call(['git', 'checkout', branch], cwd='./')

    os.chdir(currentPath)


def main(argv):
    branches = DEFAULT_BRANCHES
    if (len(argv) > 0):
        if (argv[0] == 'branch'):
            branches = argv[1:] + DEFAULT_BRANCHES
            
    os.chdir(os.getcwd() + "/../")

    if not os.path.exists(DEPENDENCIES_PATH):
        os.mkdir(DEPENDENCIES_PATH)

    # # Cloning Repos
    if not os.path.exists(PYGEPPETTO_PATH):
        clone('https://github.com/openworm/pygeppetto.git', branches, destination_folder=PYGEPPETTO_PATH)
    subprocess.call(['pip', 'install', '-e', '.'], cwd=PYGEPPETTO_PATH)

    if not os.path.exists(PYNWB_PATH):
        clone('https://github.com/NeurodataWithoutBorders/pynwb.git', branches, destination_folder=PYNWB_PATH)
    subprocess.call(['pip', 'install', '-e', '.'], cwd=PYNWB_PATH)

    if not os.path.exists(JUPYTER_EXTENSION_PATH):
        clone('https://github.com/openworm/org.geppetto.frontend.jupyter.git', branches, destination_folder=JUPYTER_EXTENSION_PATH)
        subprocess.call(['npm', 'install'], cwd=JUPYTER_EXTENSION_PATH+'js')
    subprocess.call(['npm', 'run', 'build-dev'], cwd=JUPYTER_EXTENSION_PATH+'js')


    if not os.path.exists(WEBAPP_PATH):
        clone('https://github.com/tarelli/geppetto-nwbexplorer', branches, destination_folder=WEBAPP_PATH)
        print("NPM Install and build for Geppetto Frontend  ...")
        subprocess.call(['npm', 'install'], cwd=WEBAPP_PATH)
    subprocess.call(['npm', 'run', 'build-dev'], WEBAPP_PATH)




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

    print("Installing widgetsnbextension Jupyter Extension ...")        
    subprocess.call(['jupyter', 'nbextension', 'enable', '--py', 'widgetsnbextension'],
                    cwd=JUPYTER_EXTENSION_PATH)
    print("Installing jupyter_geppetto Jupyter Server Extension ...")
    subprocess.call(['jupyter', 'serverextension', 'enable', '--py', 'jupyter_geppetto'],
                    cwd=JUPYTER_EXTENSION_PATH)

    print("Installing UI python package ...")
    subprocess.call(['pip', 'install', '-e', '.'], cwd='.')

if __name__ == "__main__":
    main(sys.argv[1:])


