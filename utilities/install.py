import os
import subprocess
import sys
from welcome import donkey

branch = None

# repos
NWBEXP = 'https://github.com/metacell/geppetto-nwbexplorer'
# PYNWB = 'https://github.com/NeurodataWithoutBorders/pynwb.git'
JUPYTER = 'https://github.com/openworm/org.geppetto.frontend.jupyter.git'
PYGEPPETTO = 'https://github.com/openworm/pygeppetto.git'
NWBWIDGETS = 'https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets.git'

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


def main(branch=branch, npmSkip=False, skipTest=False):



    if not os.path.exists(DEPS_DIR):
        os.mkdir(DEPS_DIR)
    os.chdir(DEPS_DIR)
    print(f"{donkey}\n")    
    sys.stdout.flush()
    
    # install requirements
    cprint("Installing requirements")
    execute(cmd=['pip', 'install', '-r', 'requirements.txt'], cwd=ROOT_DIR)

    # install pytest if needed
    if not skipTest:
        cprint("Installing pytest")
        if subprocess.call(['pip', 'show', 'pytest']):
            subprocess.call(['pip', 'install', 'pytest==4.6.2', 'pytest-cov==2.7.1', 'tox==3.12.1'])

    # install pygeppetto
    cprint("Installing pygeppetto")
    clone(repository=PYGEPPETTO,
          folder='pygeppetto',
          default_branch='development'
          )
    execute(cmd=['pip', 'install', '-e', '.'], cwd='pygeppetto')


    # test
    if skipTest:
        cprint("Skipping pygeppetto tests")
    else:
        cprint("Testing pygeppetto")
        execute(cmd=['coverage', 'run', '--source', 'pygeppetto', '-m', 'pytest', '-v', '-c', 'tox.ini'], cwd=os.path.join(DEPS_DIR, 'pygeppetto'))



    # # install pynwb
    # cprint("Installing pynwb")
    # clone(repository=PYNWB,
    #     folder='pynwb',
    #     default_branch='dev'
    # )
    # execute(cmd=['pip', 'install', '-e', '.'], cwd='pynwb')


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


    # test
    if skipTest:
        cprint("Skipping tests")
    else:
        cprint("Testing NWB-Explorer")
        execute(cmd=['python', '-m', 'pytest', 
            '--ignore=dependencies',
            '--ignore=test/test_reader.py',
            ], cwd=ROOT_DIR)

    
    cprint("Installing client packages")
    if not skipNpm:
        execute(cmd=['npm', 'install'], cwd=WEBAPP_DIR)
        execute(cmd=['npm', 'run', 'build-dev'], cwd=WEBAPP_DIR)


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

    parser.add_argument('--no-test', dest='skipTest', action="store_true", default=False,
                        help='Skip python tests.')

    args = parser.parse_args([arg if arg != 'branch' else '-b' for arg in sys.argv[1:]])
    print(args)
    branch = args.branch

    skipNpm = args.skipNpm
    skipTest = args.skipTest
    main(branch, skipNpm, skipTest)
