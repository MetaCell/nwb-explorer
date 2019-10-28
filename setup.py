import fnmatch
import os
from glob import glob

import setuptools

#This block copies resources to the server so we avoid jupyter nbextension install --py --sys-prefix jupyter_geppetto
data_files = []
data_files.append(('geppetto/src/main/webapp/build/', glob('src/jupyter_geppetto/geppetto/src/main/webapp/build/*.js')))
data_files.append(('geppetto/src/main/webapp/build/', glob('src/jupyter_geppetto/geppetto/src/main/webapp/build/*.vm')))
data_files.append(('geppetto/geppetto/src/main/webapp/build/', glob('src/jupyter_geppetto/geppetto/src/main/webapp/build/fonts/*')))
for root, dirnames, filenames in os.walk('src/jupyter_geppetto/geppetto/src/main/webapp/js/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append((root[3:], [os.path.join(root, filename)]))


setuptools.setup(
    name="nwb_explorer",
    version="0.3",
    url="https://github.com/tarelli/nwb-explorer",
    author="MetaCell",
    author_email="info@metacell.us",
    description="NWB Explorer User interface",
    license="MIT",
    long_description=open('README.md').read(),
    data_files=data_files,
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.hoc']
    },
    scripts=['NWBE'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'jupyter_geppetto>=1.0.0',
        'bokeh>=0.13.0',
        'holoviews>=1.10.6',
        'msgpack-python==0.5.6',
        'nose==1.3.7',
        'Pillow==5.2.0',
        'redis==2.10.6',
        'seaborn==0.8.1',
        'uuid==1.30',
        'pynwb>=1.0.3',
        'imageio>=2.5.0',
        'quantities>=0.12.3',
        'hdmf==1.1.2',
        'nwbwidgets==0.0.2'
    ],
)
