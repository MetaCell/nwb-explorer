import nwbFileService from '../services/NWBFileService';
import Utils from '../Utils';

import {
  LOAD_NWB_FILE, LOAD_NWB_FILE_IN_NOTEBOOK, NWB_FILE_LOADED, UNLOAD_NWB_FILE_IN_NOTEBOOK,
  loadedNWBFileInNotebook, loadNWBFileInNotebook 
} from '../actions/nwbfile';

import { ADD_WIDGET, UPDATE_WIDGET, ADD_PLOT_TO_EXISTING_WIDGET, updateDetailsWidget, showSweeps, showGeneral, showAcquisition, showStimulus } from '../actions/flexlayout';
import { waitData } from '../actions/general';
import { NOTEBOOK_READY, notebookReady } from '../actions/notebook';


function handleShowWidget (store, next, action) {
  // const instance = Instances.getInstance(path);
  if (action.data.type === 'TimeSeries') { // Instances.getInstance(path).getType().wrappedObj.name
    return handlePlotTimeseries(store, next, action);
  } else if (action.data.type === 'ImageSeries') { // Instances.getInstance(path).getType().wrappedObj.name
    store.dispatch(updateDetailsWidget(action.data.instancePath));
    return handleImportTimestamps(store, next, action);
  } else {
    return next(action);
  }
}

function handleImportTimestamps (store, next, action) {
  const time_path = action.data.instancePath + '.timestamps';
  const timestamps = Instances.getInstance(time_path);

  if (timestamps.getValue().wrappedObj.value.eClass == 'ImportValue') {

    store.dispatch(waitData('Loading timestamps data...', action.type));
    timestamps.getValue().getPath = () => timestamps.getPath()

    timestamps.getValue().resolve(timeValue => {      
      GEPPETTO.ModelFactory.deleteInstance(timestamps),
      Instances.getInstance(time_path)
        
      next(action);
    })
     
  } else {
    next(action);
  }
}

function handlePlotTimeseries (store, next, action) {
  // If a set of actions are passed, loop through them and execute each one independently
  if ( action.data !== undefined ) {
    if ( Array.isArray(action.data.actions) ) {
      for ( var i = 0; i < action.data.actions.length; i++ ) {
        handlePlotTimeseries(store, next, action.data.actions[i])
      }
    }
  }

  if ( action.data.instancePath === undefined ) {
    return;
  }
  
  store.dispatch(updateDetailsWidget(action.data.instancePath));
  
  const data_path = action.data.instancePath + '.data';
  let data = Instances.getInstance(data_path);
  const time_path = action.data.instancePath + '.timestamps';
  let time = Instances.getInstance(time_path);

  if (data.getValue().wrappedObj.value.eClass == 'ImportValue') {

    store.dispatch(waitData('Loading timeseries data...', action.type));
    // Trick to resolve with the instance path instead than the type path. TODO remove when fixed 
    data.getValue().getPath = () => data.getPath()
    time.getValue().getPath = () => time.getPath()

    data.getValue().resolve(dataValue => {
      time.getValue().resolve(timeValue => {      
        GEPPETTO.ModelFactory.deleteInstance(data),
        GEPPETTO.ModelFactory.deleteInstance(time),
        Instances.getInstance(data_path),
        Instances.getInstance(time_path)
        
        next(action);
      })
    });
     
  } else {
    next(action);
  }
}

const nwbMiddleware = store => next => action => {
  // console.log(action);
  switch (action.type) {

  case LOAD_NWB_FILE:
    next(action);
    Project.loadFromURL(action.data.nwbFileUrl);
    
    GEPPETTO.on('jupyter_geppetto_extension_ready', data => { // It's triggered once

      console.log("Initializing Python extension");
      
      store.dispatch(notebookReady);
           
      /*
       * 
       * Utils.execPythonMessage('utils.start_notebook_server()');
       */
    });
    break;
  

  case LOAD_NWB_FILE_IN_NOTEBOOK:
    next(action);
    nwbFileService.loadNWBFileInNotebook(store.getState().nwbfile.nwbFileUrl).then(
      () => store.dispatch(loadedNWBFileInNotebook)
    );
    
    break;

  case UNLOAD_NWB_FILE_IN_NOTEBOOK:
    next(action);
    Utils.execPythonMessage('del nwbfile');
    
    break;
      
  case NOTEBOOK_READY:
    next(action);
    // FIXME for some reason the callback for python messages is not being always called
    Utils.execPythonMessage('from nwb_explorer.nwb_main import main');
    store.dispatch(loadNWBFileInNotebook);

    break;

  case UPDATE_WIDGET:
  case ADD_WIDGET:
  case ADD_PLOT_TO_EXISTING_WIDGET:
    return handleShowWidget(store, next, action);
    
  default: next(action);
  }

  
}


export default nwbMiddleware;


