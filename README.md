[![Build Status](https://travis-ci.org/MetaCell/nwb-explorer.svg?branch=master)](https://travis-ci.org/MetaCell/nwb-explorer)
[![codecov](https://codecov.io/gh/MetaCell/nwb-explorer/branch/master/graph/badge.svg)](https://codecov.io/gh/MetaCell/nwb-explorer)
[![Twitter Follow](https://img.shields.io/twitter/follow/metacell.svg?label=follow&style=social)](https://twitter.com/metacell)

# NWB Explorer

NWB Explorer is a web application that can be used by scientists to read, visualize and explore
the content of NWB:N 2 files.

![nwbexplorer](https://user-images.githubusercontent.com/39889/67516734-24c1e380-f66f-11e9-9fba-5151118f5e4d.gif)

Learn more about the [Neurodata Without Borders](https://www.nwb.org/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing 
purposes. See deployment for notes on how to deploy the project on a live system. 

### Prerequisites

Below you will find the software you need to install to use nwb explorer (and the versions we used):

* Git (2+).
* Node (10+) and npm (6+).
* Python 3 (3.7+), pip (20+)

#### Python Dependencies

We recommend the use of a new python 3 virtual environment:

```bash
python3 -m venv nwb-explorer
source nwb-explorer/bin/activate
```

Or, with conda

```bash
conda create -n nwb-explorer python=3.9
conda activate nwb-explorer
```

### Clone "nwb-explorer" Repository

Clone repository using the development branch:

```bash
git clone -b development https://github.com/MetaCell/nwb-explorer
```

### Run via Docker

If you have Docker installed, you can run NWB explorer with one single command:

```bash
docker run -it -p8888:8888 gcr.io/metacellllc/nwb-explorer:0.6.2
```

#### Build Docker image
There is a [Dockerfile](./Dockerfile) ready to build a container for NWB-Explorer:

```bash
cd nwb-explorer
docker build -t nwb-explorer .
docker run -it -p8888:8888 nwb-explorer
```
Then, after the Docker contained has started, the application is ready at http://localhost:8888

### Local Installation without Docker

Instructions to get a development environment running.

```bash
cd nwb-explorer
python utilities/install.py
```

## How to run NWB Explorer

After the local installation is complete, run the script:

```bash
cd nwb-explorer
./NWBE
```

If everything worked, the default browser will open on `http://localhost:8888/geppetto`

## Getting started with NWB Explorer

When the application is started, no file will be loaded.

1. Use the interface to load the file from a public url or just load a sample
1. Specify the parameter nwbfile in your browser. Example: `http://localhost:8888/geppetto?nwbfile=https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb`

After the file is loaded, a Jupyter notebook will be available.
From the notebook the current loaded file can be accessed through the variable `nwbfile`.
For further information about the Python API, see the [PyNWB docs](https://pynwb.readthedocs.io/en/stable/)

### Python code from sources

In order to have all the Python files NWB:N 2 ed from sources, the application and the dependencies must be installed in development mode, i.e. with the command

```bash
pip install -e .
```

### Javascript code from sources

JS/HTML code can be found inside `webapp/`. The code needs to be rebuilt with webpack everytime there is a change. To avoid having to do so you can use the Webpack development server running in `webapp/` this command:

```bash
npm run build-dev-noTest:watch
```

This will spawn a process that while left running will watch for any changes on the `webapp` folder and automatically deploy them each time a file is saved.

To check if a dependency is installed in development mode, run `pip list`.

## Built With

* [Geppetto](http://www.geppetto.org/) - Used to build a web-based application to interpret and visualize the NWB:N 2 files.
* [PyNWB](https://github.com/NeurodataWithoutBorders/pynwb) - Used to read and manipulate NWB:N 2 files
* [Jupyter notebook](https://jupyter.org/) - Jupyter notebook is used as a backend.


## Background

The NWB Explorer was initially created by [MetaCell](http://metacell.us) to showcase the features of the [Geppetto](http://www.geppetto.org/) platform to share
neurophysiological data in [Neurodata Without Borders](https://www.nwb.org/) format. It was further developed as part of a
[Google Summer of Code](https://summerofcode.withgoogle.com/) project for the [OpenWorm project](http://openworm.org/). It is currently being extended as part of the [Open Source Brain](http://www.opensourcebrain.org/)
project to provide both a standalone and online application for visualising and analysing the contents of NWB:N 2 files.
This work is currently funded by the [Wellcome Trust](https://wellcome.ac.uk/).

## Authors

* Matteo Cantarelli ([MetaCell](http://metacell.us))
* Giovanni Idili ([MetaCell](http://metacell.us))
* Filippo Ledda ([MetaCell](http://metacell.us))
* Rodriguez Facundo ([MetaCell](http://metacell.us))
* Afonso Pinto ([MetaCell](http://metacell.us))
* Padraig Gleeson ([UCL/Open Source Brain](http://opensourcebrain.org))


See also the list of [contributors](https://github.com/Metacell/nwb-explorer/contributors) who participated in this project.
