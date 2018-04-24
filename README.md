# NWB Explorer

```
git clone https://github.com/tarelli/nwb-explorer
cd nwb-explorer
mkdir static
cd static
git clone https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp/extensions
git clone https://github.com/tarelli/geppetto-nwbexplorer
[at this stage copy the GeppettoConfiguration.json from this repo overwriting the default one inside the webapp folder]
cd ..
npm install
npm run build-dev-noTest
```

## Start the server
On OSX need to run redis server manually:
```
nohup redis-server &
```
Then run:
```
python manage.py runserver
```

Go to http://localhost:8000/ and enjoy!

## How to develop

Any change you make in the python code will be automatically redeployed by the Django server.

JS/HTML code can be found inside `static/org.geppetto.frontend/src/main/webapp/`. The code needs to be rebuilt with webpack everytime there is a change. The recommended way is to run in `/static/org.geppetto.frontend/src/main/webapp/` this command:
```
npm run build-dev-noTest:watch
```
