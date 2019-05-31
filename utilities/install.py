import os
import subprocess
import sys


def intro():
    n = 26
    delimiter = '\U0001F53D'
    print()
    print(f"{delimiter*n}")
    print()
    print(f"\U0001F604 Welcome to \033[36;3mNWB-Explorer\033[0m development installation\n")
    print(f"\U0001F463 We will execute the following steps:\n")
    print(f"  \U0001F40D Install Python requirements.\n")
    print(f"  \U0001F63C Clone some GitHub repositories\n")
    print(f"  \U0001F9D9 Setup a custom Geppetto Application:\n")
    print(f"    \U0001F41E Install frontend NPM packages.\n")
    print(f"    \U0001F9F1 Build frontend bundle.\n")
    print(f"    \U0001F316 Enable Jupyter extensions.\n")
    print(f"  \U0001F433 \033[0m Wrap-up and tag the Docker image.\n")
    print(f"\U0000231B The  whole process takes between 3 to 5 minutes. \033[0m \n")
    print(f"\U0001F3C4 Thank you for using NWB-Explorer!\n")
    print(f"{delimiter*n}\n")    
    sys.stdout.flush()

branch = None

# repos
PYECORE = 'https://github.com/rodriguez-facundo/pyecore'
NWBEXP = 'https://github.com/metacell/geppetto-nwbexplorer'
PYNWB = 'https://github.com/NeurodataWithoutBorders/pynwb.git'
JUPYTER = 'https://github.com/openworm/org.geppetto.frontend.jupyter.git'
PYGEPPETTO = 'https://github.com/openworm/pygeppetto.git'
NWBWIDGETS = 'https://github.com/jupyter-widgets/ipywidgets.git'

WEBAPP_DIR = "webapp"
JUPYTER_DIR = 'org.geppetto.frontend.jupyter'
ROOT_DIR = os.path.join(os.getcwd(), os.pardir)
DEPS_DIR = os.path.join(ROOT_DIR, 'dependencies')

def cprint(string):
    print(f"\033[35;4m\U0001f560 {string} \033[0m \n")
    sys.stdout.flush()

# by default clones branch (which can be passed as a parameter python install.py branch test_branch)
# if branch doesnt exist clones the default_branch
def clone(repository, folder, default_branch, cwdp='', recursive=False):
    global branch
    print("Cloning " + repository)
    if os.path.exists(os.path.join(cwdp, folder)):
        print(f'Skipping clone of {repository}: folder exists')
    else:
        if recursive:
            subprocess.call(['git', 'clone', '--recursive', repository], cwd='./' + cwdp)
        else:
            if folder:
                subprocess.call(['git', 'clone', repository, folder], cwd='./' + cwdp)
            else:
                subprocess.call(['git', 'clone', repository], cwd='./' + cwdp)
    checkout(folder, default_branch, cwdp)

def checkout(folder, default_branch, cwdp):
    currentPath = os.getcwd()
    print(currentPath)
    newPath = os.path.join(currentPath, cwdp, folder)
    print(newPath)
    os.chdir(newPath)
    python_git = subprocess.Popen("git branch -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outstd, errstd = python_git.communicate()
    if branch and branch in str(outstd):
        subprocess.call(['git', 'checkout', branch], cwd='./')
    else:
        subprocess.call(['git', 'checkout', default_branch], cwd='./')
    os.chdir(currentPath)

def execute(cmd, cwd='.'):
    exit_code = subprocess.call(cmd, cwd=cwd)
    if exit_code != 0:
        raise SystemExit('Error installing NWB-Explorer')


def main(branch=branch, npmSkip=False):



    if not os.path.exists(DEPS_DIR):
        os.mkdir(DEPS_DIR)
    os.chdir(DEPS_DIR)
    intro()
    
    # install requirements
    cprint("Installing requirements")
    execute(cmd=['pip', 'install', '-r', 'requirements.txt'], cwd=ROOT_DIR)

    # install pyecore
    cprint("Installing pyecore")
    clone(repository=PYECORE,
          folder='pyecore',
          default_branch='develop'
          )
    execute(cmd=['pip', 'install', '-e', '.'], cwd='pyecore')

    # install pygeppetto
    cprint("Installing pygeppetto")
    clone(repository=PYGEPPETTO,
        folder='pygeppetto',
        default_branch='development'
    )
    execute(cmd=['pip', 'install', '-e', '.'], cwd='pygeppetto')



    # install pynwb
    cprint("Installing pynwb")
    clone(repository=PYNWB,
        folder='pynwb',
        default_branch='dev'
    )
    execute(cmd=['pip', 'install', '-e', '.'], cwd='pynwb')

    # install pynwb
    cprint("Installing nwb jupyter widgets")
    clone(repository=NWBWIDGETS,
          folder='nwbwidgets',
          default_branch='master'
          )
    subprocess.call(['pip', 'install', '-e', '.'], cwd='nwbwidgets')

    # install jupyter notebook
    cprint("Installing org.geppetto.frontend.jupyter")
    clone(repository=JUPYTER,
        folder='org.geppetto.frontend.jupyter',
        default_branch='development'
    )
    if not skipNpm:
        execute(cmd=['npm', 'install'], cwd=os.path.join(JUPYTER_DIR, 'js'))
        execute(cmd=['npm', 'run', 'build-dev'], cwd=os.path.join(JUPYTER_DIR, 'js'))



    # install nwb explorer
    os.chdir(ROOT_DIR)
    cprint("Installing nwb-explorer frontend")
    clone(repository=NWBEXP,
        folder=WEBAPP_DIR,
        default_branch='development'
    )
    if not skipNpm:
        execute(cmd=['npm', 'install'], cwd=WEBAPP_DIR)
        execute(cmd=['npm', 'run', 'build-dev'], cwd=WEBAPP_DIR)



    # back to finish jupyter installation
    cprint("Installing extensions")
    # FIXME for some reason it fails the first time on a clean conda env 
    # (pip version, conda version, jupyter installation?)
    if subprocess.call(['pip', 'install', '-e', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR)):
        execute(cmd=['pip', 'install', '-e', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR))

    execute(cmd=['jupyter', 'nbextension', 'install', '--py', '--symlink', '--sys-prefix', 'jupyter_geppetto'])
    execute(cmd=['jupyter', 'nbextension', 'enable', '--py', '--sys-prefix', 'jupyter_geppetto'])
    execute(cmd=['jupyter', 'nbextension', 'enable', '--py', '--sys-prefix', 'widgetsnbextension'])
    execute(cmd=['jupyter', 'serverextension', 'enable', '--py', '--sys-prefix', 'jupyter_geppetto'])



    # install app
    cprint("Installing UI python package...")
    execute(cmd=['pip', 'install', '-e', '.', '--no-deps'])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install NWB explorer and related dev libraries.')
    parser.add_argument('--branch', '-b', dest='branch', type=str, action="store", nargs='?',
                        help='the branch to checkout for all projects. '
                             'The branch is checked out if exists, otherwise the default for the project will be used')
    parser.add_argument('--npm-skip', dest='skipNpm', action='store_true', default=False,
                        help='Skips the long npm install and build processes')

    args = parser.parse_args([arg if arg != 'branch' else '-b' for arg in sys.argv[1:]])
    print(args)
    branch = args.branch

    skipNpm = args.skipNpm
    main(branch, skipNpm)
