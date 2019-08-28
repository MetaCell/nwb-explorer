import { 
  RAISE_ERROR, 
  RECOVER_FROM_ERROR,
  WAIT_DATA
} from '../actions/general';

import { NWB_FILE_NOT_FOUND_ERROR,MODULE_NOT_FOUND_ERROR, NAME_ERROR } from 'constants';
import * as nwbfileActions from '../actions/nwbfile';
import * as notebookActions from '../actions/notebook';

function isEmbeddedInIframe () {
  return window.location !== window.parent.location;
}

export const GENERAL_DEFAULT_STATUS = { 
  embedded: isEmbeddedInIframe(),
  toggleInfoPanel: false,
  loading: false,
  error: undefined
};

export default ( state = {}, action ) => ({ 
  ...state, 
  ...reduceGeneral(state, action) 
});

function reduceGeneral (state, action) {
  switch (action.type) {

  case WAIT_DATA:
    return { loading: { ...state.loading, [action.data.offAction] : action.data.message } }
  
  case RAISE_ERROR:
    return { error: action.error }

  case RECOVER_FROM_ERROR:{
    switch (state.error.ename) {
      
    case NWB_FILE_NOT_FOUND_ERROR:
      return { error: false }
  
    case MODULE_NOT_FOUND_ERROR:
      return { error: false }
    
    case NAME_ERROR:
      return { error: false }
    default:
      return { error: false }
    }
  }


  case nwbfileActions.LOAD_NWB_FILE:
    return { loading: { ...state.loading, [nwbfileActions.NWB_FILE_LOADED] : 'Loading NWB file' } }
  
  case nwbfileActions.LOAD_NWB_FILE_IN_NOTEBOOK: 
    return { loading: { ...state.loading, [nwbfileActions.LOADED_NWB_FILE_IN_NOTEBOOK] : 'Loading NWB file into Python notebook' } }
  
  case notebookActions.LOAD_NOTEBOOK:
    return {
      loading: {
        ...state.loading, 
        [notebookActions.NOTEBOOK_READY] : 'Initializing Python notebook'  
      }, 
      showNotebook: true, 
      isNotebookReady: false
    }
  
  default:{
    const loading = { ...state.loading };
    if (loading[action.type]) {
      delete loading[action.type];
    }
    return { loading: loading };
  }

  }
}
