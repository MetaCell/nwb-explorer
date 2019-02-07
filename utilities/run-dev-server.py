import subprocess
subprocess.call(['npm', 'install'], cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/')
subprocess.call(['npm', 'run', 'build-dev-noTest:watch'], cwd='../org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/')
