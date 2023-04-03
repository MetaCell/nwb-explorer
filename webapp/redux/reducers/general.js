import {
  RAISE_ERROR,
  RECOVER_FROM_ERROR,
  WAIT_DATA,
  OPEN_DIALOG,
  CLOSE_DIALOG
} from "../actions/general";

import {
  NWB_FILE_NOT_FOUND_ERROR,
  MODULE_NOT_FOUND_ERROR,
  NAME_ERROR
} from "../../constants";
import * as nwbfileActions from "../actions/nwbfile";
import * as notebookActions from "../actions/notebook";

import { isEmbeddedInIframe } from "../../Utils";

export const GENERAL_DEFAULT_STATUS = {
  embedded: isEmbeddedInIframe(),
  toggleInfoPanel: false,
  loading: false,
  error: undefined
};

export default (state = {}, action) => ({
  ...state,
  ...reduceGeneral(state, action)
});

function reduceGeneral (state, action) {
  switch (action.type) {
  case WAIT_DATA:
    return {
      loading: {
        ...state.loading,
        [action.data.offAction]: action.data.message
      }
    };

  case RAISE_ERROR:
    return { error: action.error };

  case RECOVER_FROM_ERROR: {
    return { error: false };
  }

  case nwbfileActions.LOAD_NWB_FILE_IN_NOTEBOOK:
    return state; // { loading: { ...state.loading, [nwbfileActions.LOADED_NWB_FILE_IN_NOTEBOOK] : 'Loading NWB file into Python notebook' } }

  case notebookActions.LOAD_NOTEBOOK:
    return {
      showNotebook: true,
      isNotebookReady: false
    };

  case OPEN_DIALOG:
    return {
      ...state,
      dialogOpen: true,
      dialogTitle: action.payload.title,
      dialogMessage: action.payload.message
    };

  case CLOSE_DIALOG:
    return { ...state, dialogOpen: false };

  default:
    return state;
  }
}
