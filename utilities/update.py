import subprocess

# Hack so that it works in python 2 and 3
try:
    input = raw_input
except NameError:
    pass
reply = eval(input(
    "Any uncommited change to your jupyter notebook will be stashed. Are you sure you want to update HNN-UI? (y/n)"))

if reply[0] == 'y':
    # Checking out repos
    subprocess.call(['git', 'pull'])
    subprocess.call(['git', 'checkout', 'development'], cwd='../org.geppetto.frontend.jupyter')
    subprocess.call(['git', 'pull'], cwd='../org.geppetto.frontend.jupyter')
    subprocess.call(['git', 'checkout', 'development'],
                    cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/')
    subprocess.call(['git', 'pull'], cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/')
    subprocess.call(['git', 'checkout', 'development'],
                    cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/extensions/geppetto-hnn/')
    subprocess.call(['git', 'pull'],
                    cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/extensions/geppetto-hnn/')

    # Installing and building the frontend
    subprocess.call(['npm', 'install'],
                    cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/')
    subprocess.call(['npm', 'run', 'build-dev-noTest'],
                    cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/')

else:
    print("Exit without updating")
