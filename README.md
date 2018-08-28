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

  

 
### Installing

A step by step instructions to get a development env running

```
git clone -b development https://github.com/tarelli/nwb-explorer
cd nwb-explorer
mkdir static
cd static
git clone -b development https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp/extensions
git clone https://github.com/tarelli/geppetto-nwbexplorer
cd ..
/bin/cp -rf ../../../../../GeppettoConfiguration.json .
npm install
npm run build-dev-noTest
```

#### Adding a local nwb file folder:

```
mkdir test_data <- In the nwb-explorer folder
cd test_data/
wget http://ec2-34-229-132-127.compute-1.amazonaws.com/api/v1/item/5ae9f7896664c640660400b5/download -O brain_observatory.nwb

```

#### Python Dependencies

We recommend the use of a new python virtual environment: 

```
python3 -m venv new_venv_folder
source new_venv_folder/bin/activate
pip install -r requirements.txt
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



