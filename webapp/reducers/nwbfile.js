import * as nwbfileActions from '../actions/nwbfile';
import * as notebookActions from '../actions/notebook';

export const NWBFILE_DEFAULT_STATUS = {
  nwbFileUrl: null,
  model: null,
  isLoadedInNotebook: false,
  isLoadingInNotebook: false,
  modelSettings: {}
};


export default ( state = {}, action ) => ({ ...state, ...reduceNWBFile(state, action) });

function reduceNWBFile (state = {}, action) {
  switch (action.type) {
    
  case nwbfileActions.SET_NWB_FILE:
    return { ...action.data }
  
  case nwbfileActions.LOAD_NWB_FILE:
    return { ...action.data, nwbFileLoading: true }

  case nwbfileActions.LOAD_NWB_FILE_IN_NOTEBOOK:
    return { 
      isLoadedInNotebook: false, 
      isLoadingInNotebook: true, 
    }

  case nwbfileActions.UNLOAD_NWB_FILE_IN_NOTEBOOK:
    return { isLoadedInNotebook: false }
  
  case nwbfileActions.LOADED_NWB_FILE_IN_NOTEBOOK:
    return { isLoadedInNotebook: true, isLoadingInNotebook: false }
  
  case nwbfileActions.UNLOAD_NWB_FILE:
    return {
      nwbFileUrl: null, 
      model: null 
    }

  case nwbfileActions.NWB_FILE_LOADED:
    return { model: true, nwbFileLoading: false }  

  case nwbfileActions.CLEAR_MODEL:
    return { model: null }
  
  case notebookActions.NOTEBOOK_READY:
    return { isLoadingInNotebook: false }
  

  default:
    return state;
  }
}