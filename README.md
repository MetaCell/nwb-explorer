# NWB Explorer

NWB Explorer is an application that can be used by scientists to read, visualize and explore
the content of NWB 2 files. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites 
Below you will find the software you need to install to use nwb explorer (and the versions we used)
* Git (2.17.0).
* Node (9.11.1) and npm (6.0.0).
* Redis-Server (4.0.9).
* Python 3 (3.6.5), pip (10.0.1) and Python3-tk.
#### Python Dependencies
 `pip install -r requirements.txt`

or

* Django (1.9). `pip install django`
* Pygeppeto_server. ```git clone https://github.com/MetaCell/pygeppetto-django.git && cd pygeppetto-django && git checkout development && pip install -e . ```
* Pygeppeto_model.```git clone https://github.com/openworm/pygeppetto.git && cd pygeppetto && git checkout manager && pip install -e . ```
* Pyecore (0.8.1). `pip install pyecore`
* Pynwb. ```git clone https://github.com/NeurodataWithoutBorders/pynwb.git && cd pynwb && git checkout dev && pip install -e . ```
* Seaborn (0.8.1). `pip install seaborn`
* Holoviews (1.10.6). `pip install holoviews`
* Pillow (5.2.0). `pip install Pillow`
 
### Installing

A step by step instructions to get a development env running

```
git clone https://github.com/tarelli/nwb-explorer
cd nwb-explorer
mkdir static
cd static
git clone https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp/extensions
git clone https://github.com/tarelli/geppetto-nwbexplorer
cd ..
/bin/cp -rf ../../../../../GeppettoConfiguration.json .
npm install
npm run build-dev-noTest
```
## Deployment

Run the redis-server manually:

OSX
```
nohup redis-server &
```
Linux
```
redis-server &
```
Then, on the nwb-explorer folder, run :
```
python manage.py runserver
```

## How to use

![Real plots](https://github.com/NeurodataWithoutBorders/nwb_hackathons/raw/master/HCK04_2018_Seattle/Projects/NWBExplorer/nwbexplorer.gif)
## How to develop

Any change you make in the python code will be automatically redeployed by the Django server.

JS/HTML code can be found inside `static/org.geppetto.frontend/src/main/webapp/`. The code needs to be rebuilt with webpack everytime there is a change. The recommended way is to run in `/static/org.geppetto.frontend/src/main/webapp/` this command:
```
npm run build-dev-noTest:watch
```

## Running the tests

```
python manage.py test
```
## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Geppetto](http://www.geppetto.org/) - Used to build a web-based application to visualize and simulate the NWB 2.0 files.


## Authors

* Matteo Cantarelli ([MetaCell](http://metacell.us))
* Giovanni Idili ([MetaCell](http://metacell.us))

See also the list of [contributors](https://github.com/tarelli/nwb-explorer/contributors) who participated in this project.



