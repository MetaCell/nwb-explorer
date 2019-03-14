import os
import subprocess
import sys
from shutil import copyfile
import pkg_resources

branch = None

# repos
NWBEXP = 'https://github.com/metacell/geppetto-nwbexplorer'
PYNWB = 'https://github.com/NeurodataWithoutBorders/pynwb.git'
JUPYTER = 'https://github.com/openworm/org.geppetto.frontend.jupyter.git'
PYGEPPETTO = 'https://github.com/openworm/pygeppetto.git'

WEBAPP_DIR = "webapp"
JUPYTER_DIR = 'org.geppetto.frontend.jupyter'
ROOT_DIR = os.path.join(os.getcwd(), os.pardir)
DEPS_DIR = os.path.join(ROOT_DIR, 'dependencies')

def cprint(string):
    print(f"\033[35;4m\U0001f560 {string} \033[0m \n")
    sys.stdout.flush()

# by default clones branch (which can be passed as a parameter python install.py branch test_branch)
# if branch doesnt exist clones the default_branch
def clone(repository, folder, default_branch, cwdp='', recursive=False, destination_folder=None):
    global branch
    print("Cloning " + repository)
    if recursive:
        subprocess.call(['git', 'clone', '--recursive', repository], cwd='./' + cwdp)
    else:
        if destination_folder:
            subprocess.call(['git', 'clone', repository, destination_folder], cwd='./' + cwdp)
        else:
            subprocess.call(['git', 'clone', repository], cwd='./' + cwdp)
    checkout(folder, default_branch, cwdp)

def checkout(folder, default_branch, cwdp):
    currentPath = os.getcwd()
    print(currentPath)
    newPath = currentPath + "/" + cwdp + folder
    print(newPath)
    os.chdir(newPath)
    python_git = subprocess.Popen("git branch -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    if not os.path.exists(DEPS_DIR):
        os.mkdir(DEPS_DIR)
    os.chdir(DEPS_DIR)

    # install requirements
    cprint("Installing requirements")
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'], cwd=ROOT_DIR)

    # install pygeppetto
    cprint("Installing pygeppetto")
    clone(repository=PYGEPPETTO,
        folder='pygeppetto',
        default_branch='development'
    )
    subprocess.call(['pip', 'install', '-e', '.'], cwd='pygeppetto')



    # install pynwb
    cprint("Installing pynwb")
    clone(repository=PYNWB,
        folder='pynwb',
        default_branch='dev'
    )
    subprocess.call(['pip', 'install', '-e', '.'], cwd='pynwb')



    # install jupyter notebook
    cprint("Installing org.geppetto.frontend.jupyter")
    clone(repository=JUPYTER,
        folder='org.geppetto.frontend.jupyter',
        default_branch='development'
    )
    subprocess.call(['npm', 'install'], cwd=os.path.join(JUPYTER_DIR, 'js'))
    subprocess.call(['npm', 'run', 'build-dev'], cwd=os.path.join(JUPYTER_DIR, 'js'))



    # install nwb explorer
    os.chdir(ROOT_DIR)
    cprint("Installing nwb-explorer")
    clone(repository=NWBEXP,
        folder=WEBAPP_DIR,
        destination_folder=WEBAPP_DIR,
        default_branch='development'
    )
    subprocess.call(['npm', 'install'], cwd=WEBAPP_DIR)
    subprocess.call(['npm', 'run', 'build-dev'], cwd=WEBAPP_DIR)



    # back to finish jupyter installation
    cprint("Installing extensions")
    subprocess.call(['pip', 'install', '-e', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR))
    subprocess.call(['jupyter', 'nbextension', 'install', '--py', '--symlink', '--sys-prefix', 'jupyter_geppetto'])
    subprocess.call(['jupyter', 'nbextension', 'enable', '--py', '--sys-prefix', 'jupyter_geppetto'])
    subprocess.call(['jupyter', 'nbextension', 'enable', '--py', '--sys-prefix', 'widgetsnbextension'])
    subprocess.call(['jupyter', 'serverextension', 'enable', '--py', '--sys-prefix', 'jupyter_geppetto'])



    # install app
    cprint("Installing UI python package...")
    subprocess.call(['pip', 'install', '-e', '.', '--no-deps'])