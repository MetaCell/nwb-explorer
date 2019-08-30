import nwbFileService from '../services/NWBFileService';
import Utils from '../Utils';

import {
  LOAD_NWB_FILE, LOAD_NWB_FILE_IN_NOTEBOOK, NWB_FILE_LOADED, UNLOAD_NWB_FILE_IN_NOTEBOOK,
  loadedNWBFileInNotebook, loadNWBFileInNotebook 
} from '../actions/nwbfile';

import { ADD_WIDGET, UPDATE_WIDGET, ADD_PLOT_TO_EXISTING_WIDGET, updateDetailsWidget, showSweeps } from '../actions/flexlayout';
import { waitData } from '../actions/general';
import { NOTEBOOK_READY } from '../actions/notebook';


function handleShowWidget (store, next, action) {
  // const instance = Instances.getInstance(path);
  if (action.data.type === 'TimeSeries') { // Instances.getInstance(path).getType().wrappedObj.name
    store.dispatch(updateDetailsWidget(action.data.instancePath));
    return handlePlotTimeseries(store, next, action);
  }
  if (action.data.type === 'ImageSeries') { // Instances.getInstance(path).getType().wrappedObj.name
    store.dispatch(updateDetailsWidget(action.data.instancePath));
    return handleImportTimestamps(store, next, action);
  }
  return next(action);
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
  switch (action.type) {

  case LOAD_NWB_FILE:
    Project.loadFromURL(action.data.nwbFileUrl);
    break;
  case NWB_FILE_LOADED:
    

    if (Instances.getInstance('nwbfile.sweep_table')) {
      store.dispatch(showSweeps);
    }
    break;

  case LOAD_NWB_FILE_IN_NOTEBOOK:
    nwbFileService.loadNWBFileInNotebook(store.getState().nwbfile.nwbFileUrl).then(
      () => store.dispatch(loadedNWBFileInNotebook)
    );
    break;

  case UNLOAD_NWB_FILE_IN_NOTEBOOK:
    Utils.execPythonMessage('del nwbfile');
    break;
      
  case NOTEBOOK_READY:
    // FIXME for some reason the callback for python messages is not being always called
    Utils.execPythonMessage('from nwb_explorer.nwb_main import main');
    store.dispatch(loadNWBFileInNotebook);
    break;

  case UPDATE_WIDGET:
  case ADD_WIDGET:
    return handleShowWidget(store, next, action);
  
  case ADD_PLOT_TO_EXISTING_WIDGET:
    return handlePlotTimeseries(store, next, action)
  }
  

  next(action);
}


export default nwbMiddleware;


