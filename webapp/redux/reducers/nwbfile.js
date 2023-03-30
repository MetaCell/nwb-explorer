import * as nwbfileActions from '../actions/nwbfile';
import * as notebookActions from '../actions/notebook';
import * as LayoutActions from '@metacell/geppetto-meta-client/common/layout/actions';
import { nextColor } from '../../Utils';

export const NWBFILE_DEFAULT_STATUS = {
  nwbFileUrl: null,
  model: null,
  isLoadedInNotebook: false,
  isLoadingInNotebook: false,
  modelSettings: {},
};

export default (state = {}, action) => {
  switch (action.type) {
  case nwbfileActions.SET_NWB_FILE:
    return { ...state, ...action.data };

  case nwbfileActions.LOAD_NWB_FILE: {
    return { ...state, nwbFileUrl: action.data.nwbFileUrl, nwbFileLoading: true };
  }
  case nwbfileActions.LOAD_NWB_FILE_IN_NOTEBOOK:
    return {
      ...state,
      isLoadedInNotebook: false,
      isLoadingInNotebook: true,
    };

  case nwbfileActions.UNLOAD_NWB_FILE_IN_NOTEBOOK:
    return { ...state, isLoadedInNotebook: false };

  case nwbfileActions.LOADED_NWB_FILE_IN_NOTEBOOK:
    return { ...state, isLoadedInNotebook: true, isLoadingInNotebook: false };

  case nwbfileActions.UNLOAD_NWB_FILE:
    return {
      ...state,
      nwbFileUrl: null,
      model: null,
    };

  case nwbfileActions.NWB_FILE_LOADED:
    return { ...state, model: true, nwbFileLoading: false };

  case nwbfileActions.CLEAR_MODEL:
    return { ...state, model: null };

  case notebookActions.NOTEBOOK_READY:
    return { ...state, isLoadingInNotebook: false };
  case nwbfileActions.UPDATE_SETTINGS: {
    return { ...state, modelSettings: { ...state.modelSettings, [action.data.path]: { ...action.data } } };
  }
  case LayoutActions.layoutActions.ADD_WIDGET: {
    if (action.data.instancePaths && action.data.type === 'TimeSeries') {
      const modelSettings = { ...state.modelSettings };
      for (const path of action.data.instancePaths) {
        if (!state.modelSettings[path]) {
          const color = nextColor();
          modelSettings[path] = { color };
        }
      }
      return { ...state, modelSettings };
    }
    return state;
  }
  case LayoutActions.layoutActions.ADD_PLOT_TO_EXISTING_WIDGET: {
    const path = action.data.instancePath;
    if (!state.modelSettings[path]) {
      const modelSettings = { ...state.modelSettings };
      const color = nextColor();
      modelSettings[path] = { color };
      return { ...state, modelSettings };
    }
    return state;
  }
  default:
    return state;
  }
};
