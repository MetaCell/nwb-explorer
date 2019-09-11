from .install import DEPS_DIR, os, cprint, JUPYTER_DIR, WEBAPP_DIR, subprocess, ROOT_DIR


if __name__ == '__main__':
    os.chdir(DEPS_DIR)

    # install pygeppetto
    cprint("Installing pygeppetto")
    subprocess.call(['pip', 'install', '-e', '.'], cwd='pygeppetto')

    # install pynwb
    cprint("Installing pynwb")

    subprocess.call(['pip', 'install', '-e', '.'], cwd='pynwb')

    # install jupyter notebook
    cprint("Installing org.geppetto.frontend.jupyter")

    subprocess.call(['npm', 'run', 'build-dev'], cwd=os.path.join(JUPYTER_DIR, 'js'))

    # install nwb explorer
    os.chdir(ROOT_DIR)
    cprint("Installing nwb-explorer")
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