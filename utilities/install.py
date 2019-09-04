import os
import subprocess
import sys


branch = None

HERE = os.path.dirname(os.path.abspath(__file__))

# repos
JUPYTER = 'https://github.com/openworm/org.geppetto.frontend.jupyter.git'
PYGEPPETTO = 'https://github.com/openworm/pygeppetto.git'
NWBWIDGETS = 'https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets.git'

WEBAPP_DIR = "webapp"
JUPYTER_DIR = 'org.geppetto.frontend.jupyter'
ROOT_DIR = os.path.join(HERE, os.pardir)
DEPS_DIR = os.path.join(ROOT_DIR, 'src')

def cprint(string):
    print(f"\033[35;4m\U0001f560 {string} \033[0m \n")
    sys.stdout.flush()

# by default clones branch (which can be passed as a parameter python install.py branch test_branch)
# if branch doesnt exist clones the default_branch_or_tag
def clone(repository, folder, default_branch_or_tag, cwdp='', recursive=False):
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
    checkout(folder, default_branch_or_tag, cwdp)


def checkout(folder, default_branch_or_tag, cwdp):
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
        subprocess.call(['git', 'checkout', default_branch_or_tag], cwd='./')
    os.chdir(currentPath)

def execute(cmd, cwd='.'):
    exit_code = subprocess.call(cmd, cwd=cwd)
    if exit_code != 0:
        raise SystemExit('Error installing NWB-Explorer')


def main(branch=branch, skipNpm=False, skipTest=False, development=False):

    if not os.path.exists(DEPS_DIR):
        os.mkdir(DEPS_DIR)
    os.chdir(DEPS_DIR)
    print(f"{steps()}\n")
    sys.stdout.flush()
    
    # install requirements
    cprint("Installing requirements")
    execute(cmd=['pip', 'install', '-r', 'requirements.txt'], cwd=ROOT_DIR)

    # install pytest if needed
    if not skipTest:
        cprint("Installing test libraries")
        execute(cmd=['pip', 'install', '-r', 'requirements-test.txt'], cwd=ROOT_DIR)

    if development:
        # install pygeppetto
        cprint("Installing pygeppetto")
        clone(repository=PYGEPPETTO,
              folder='pygeppetto',
              default_branch_or_tag='development'
              )
        execute(cmd=['pip', 'install', '-e', '.'], cwd='pygeppetto')

        # test
        if skipTest:
            cprint("Skipping pygeppetto tests")
        else:
            cprint("Testing pygeppetto")
            execute(cmd=['coverage', 'run', '--source', 'pygeppetto', '-m', 'pytest', '-v', '-c', 'tox.ini'],
                    cwd=os.path.join(DEPS_DIR, 'pygeppetto'))

        # install jupyter widgets
        cprint("Installing nwb jupyter widgets")
        clone(repository=NWBWIDGETS,
              folder='nwbwidgets',
              default_branch_or_tag='master'
              )
        subprocess.call(['git', 'reset', '--hard', '9756e601b2c99384b4dc6a4fc1a164f1990d7b1b'], cwd='nwbwidgets')
        subprocess.call(['pip', 'install', '-e', '.'], cwd='nwbwidgets')

        # install jupyter geppetto
        cprint("Installing org.geppetto.frontend.jupyter")
        clone(repository=JUPYTER,
              folder='org.geppetto.frontend.jupyter',
              default_branch_or_tag='development'
              )
    if not skipNpm and os.path.exists(JUPYTER_DIR):
        execute(cmd=['npm', 'install'], cwd=os.path.join(JUPYTER_DIR, 'js'))
        execute(cmd=['npm', 'run', 'build-dev' if development else 'build'], cwd=os.path.join(JUPYTER_DIR, 'js'))


    os.chdir(ROOT_DIR)
    cprint("Installing extensions")
    # FIXME for some reason it fails the first time on a clean conda env 
    # (pip version, conda version, jupyter installation?)
    if development:
        if subprocess.call(['pip', 'install', '-e', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR)):
            execute(cmd=['pip', 'install', '-e', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR))
    else:
        if subprocess.call(['pip', 'install', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR)):
            execute(cmd=['pip', 'install', '.'], cwd=os.path.join(DEPS_DIR, JUPYTER_DIR))

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
        execute(cmd=['npm', 'run', 'build-dev' if development else 'build'], cwd=WEBAPP_DIR)


    # install app
    cprint("Installing UI python package...")
    if development:
        execute(cmd=['pip', 'install', '-e', '.', '--no-deps'])
    else:
        execute(cmd=['pip', 'install', '.', '--no-deps'])


def steps():
    return f'''\033[0m {'_' * (58)}
    (                                                           )
    (  \U0001F604 Welcome to \033[36;3mNWB-Explorer\033[0m development installation      )
    (                                                           )
    (  \U0001F463 We will execute the following steps:                  )
    (                                                           )
    (    \U0001F40D Install Python requirements.                        )
    (                                                           )
    (    \U0001F63C Clone some GitHub repositories                      )
    (                                                           )
    (    \U0001F9D9  Setup a custom Geppetto Application:                )
    (                                                           )
    (      \U0001F41E Install frontend NPM packages.                    )
    (                                                           )
    (      \U0001F9F1  Build frontend bundle.                            )
    (                                                           )
    (      \U0001F316 Enable Jupyter extensions.                        )
    (                                                           )
    (      \U0001F52C Test NWB-Explorer.                                )
    (                                                           )
    (    \U0001F433  Wrap-up and tag the Docker image.                  )
    (                                                           )
    (  \U0000231B The  whole process takes between 3 to 5 minutes.      )
    (                                                           )
    (  \U0001F3C4 Thank you for using NWB-Explorer!                     )
    ({"_" * 59})
              o
               o   ^__^
                o  (oo)\_________
                   (__)\         )\\/\\
                       ||------W |
                       ||       ||
    '''


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

    parser.add_argument('--dev', dest='development', action="store_true", default=False,
                        help='Install for development.')

    args = parser.parse_args([arg if arg != 'branch' else '-b' for arg in sys.argv[1:]])
    print(args)
    branch = args.branch

    skipNpm = args.skipNpm
    skipTest = args.skipTest
    development = args.development
    main(branch, skipNpm, skipTest, development)
