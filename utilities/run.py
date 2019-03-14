'''
Run this to debug
'''
import sys
import os
from notebook.notebookapp import main, NotebookApp


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/../')
    sys.argv.append('--NotebookApp.default_url=/geppetto')
    sys.argv.append("--NotebookApp.token=''")
    sys.argv.append('--library=nwb_explorer')

    app = NotebookApp.instance()
    app.initialize(sys.argv)
    app.file_to_run = ''
    sys.exit(app.start())

