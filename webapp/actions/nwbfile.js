export const SET_NWB_FILE = 'SET_NWB_FILE';
export const LOAD_NWB_FILE = 'LOAD_NWB_FILE';
export const NWB_FILE_LOADED = 'NWB_FILE_LOADED';
export const UNLOAD_NWB_FILE = 'UNLOAD_NWB_FILE';
export const LOAD_NWB_FILE_IN_NOTEBOOK = 'LOAD_NWB_FILE_IN_NOTEBOOK';
export const LOADED_NWB_FILE_IN_NOTEBOOK = 'LOADED_NWB_FILE_IN_NOTEBOOK';
export const UNLOAD_NWB_FILE_IN_NOTEBOOK = 'UNLOAD_NWB_FILE_IN_NOTEBOOK';
export const CLEAR_MODEL = 'CLEAR_MODEL';


export function loadNWBFile (nwbFileUrl) {
  
  return {
    type: LOAD_NWB_FILE,
    data: { nwbFileUrl: nwbFileUrl }
  }
}

export const loadNWBFileInNotebook = { type: LOAD_NWB_FILE_IN_NOTEBOOK };


export const loadedNWBFileInNotebook = { type: LOADED_NWB_FILE_IN_NOTEBOOK };


export function unloadNWBFileInNotebook () {
  
  return { type: UNLOAD_NWB_FILE_IN_NOTEBOOK, };
}

export const unloadNWBFile = { type: UNLOAD_NWB_FILE }

export function nwbFileLoaded (model) { 
  return {
    type: NWB_FILE_LOADED,
    data: { model: model.wrappedObj }
  }
}


export const clearModel = () => ({ type: CLEAR_MODEL })