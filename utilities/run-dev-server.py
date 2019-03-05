import subprocess
subprocess.call(['npm', 'install'], cwd='../webapp/')
subprocess.call(['npm', 'run', 'build-dev-noTest:watch'], cwd='../webapp/')
