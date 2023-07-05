import nwbFileService from "../../services/NWBFileService";
import Utils, { nextColor } from "../../Utils";

import {
  LOAD_NWB_FILE,
  LOAD_NWB_FILE_IN_NOTEBOOK,
  NWB_FILE_LOADED,
  UNLOAD_NWB_FILE_IN_NOTEBOOK,
  loadedNWBFileInNotebook,
  loadNWBFileInNotebook,
  nwbFileLoaded
} from "../actions/nwbfile";

import * as GeppettoActions from "@metacell/geppetto-meta-client/common/actions/actions";
import * as LayoutActions from "@metacell/geppetto-meta-client/common/layout/actions";

import MessageSocket from "@metacell/geppetto-meta-client/communication/MessageSocket";

import {
  ADD_WIDGET,
  UPDATE_WIDGET,
  ADD_PLOT_TO_EXISTING_WIDGET,
  updateDetailsWidget,
  showSweeps,
  showAcquisition,
  showStimulus,
  showProcessing
} from "../actions/widgets";
import { waitData, raiseError, RECOVER_FROM_ERROR } from "../actions/general";
import { NOTEBOOK_READY, notebookReady } from "../actions/notebook";

import { WidgetStatus } from "@metacell/geppetto-meta-client/common/layout/model";

import { getNotebookPath } from "../../services/NotebookService";

export const DEFAULT_WIDGETS = {
  python: {
    id: "python",
    name: "Python",
    status: WidgetStatus.MINIMIZED,
    icon: "fa-python",
    component: "PythonConsole",
    panelName: "bottomPanel",
    enableClose: false,
    config: {
      pythonNotebookPath: getNotebookPath(true, true),
      extensionLoaded: true
    }
  },
  general: {
    id: "general",
    name: "General",
    status: WidgetStatus.ACTIVE,
    component: "Metadata",
    panelName: "leftPanel",
    enableClose: false,
    pos: 1,
    config: { instancePath: "tmp" }
  },

  details: {
    id: "details",
    name: "Details",
    config: { instancePath: "" },
    status: WidgetStatus.HIDDEN,
    component: "Metadata",
    panelName: "leftPanel",
    enableClose: false,
    showObjectInfo: true,
    pos: 2
  }
};


/**
 * Override standard Manager
 *
 */
export async function resolveImportValue (typePath, callback) {
  const params = {};
  params.experimentId = -1;
  params.projectId = window.Project.id;
  // replace client naming first occurrence - the server doesn't know about it
  params.path = typePath.replace(`${GEPPETTO.Resources.MODEL_PREFIX_CLIENT}.`, '');

  const requestID = MessageSocket.send('resolve_import_value', params, callback);

}

function handleShowWidget (store, next, action) {
  // const instance = Instances.getInstance(path);
  if (action.data.type === "TimeSeries") {
    // Instances.getInstance(path).getType().wrappedObj.name
    return handlePlotTimeseries(store, next, action);
  }
  if (action.data.type === "ImageSeries") {
    // Instances.getInstance(path).getType().wrappedObj.name
    action.data.config.showDetail
      && store.dispatch(updateDetailsWidget(action.data.config.instancePath));
    return handleImportTimestamps(store, next, action);
  }
  if (action.data.id) {
    return next(action);
  }
}

function fileLoadedLayout () {
  const widgets = [];

  if (
    Instances.getInstance("nwbfile.stimulus")
    && Instances.getInstance("nwbfile.stimulus")
      .getType()
      .getVariables().length
  ) {
    widgets.push(showStimulus.data);
  }

  if (Instances.getInstance("nwbfile.acquisition")) {
    widgets.push(showAcquisition.data);
  }

  if (Instances.getInstance("nwbfile.sweep_table")) {
    widgets.push(showSweeps.data);
  }

  if (
    Instances.getInstance("nwbfile.processing")
    && Instances.getInstance("nwbfile.processing")
      .getType()
      .getVariables().length
  ) {
    widgets.push(showProcessing.data);
  }

  return widgets;
}

async function handlePlotTimeseries (store, next, action) {
  // If a set of actions are passed, loop through them and execute each one independently

  async function retrieveImportValue (data, data_path) {
    return new Promise((resolve, reject) => {
      resolveImportValue(data.getPath(), dataValue => {
        // next(GeppettoActions.clientActions.deleteInstance(data));
        Instances.getInstance(data_path);
        resolve();
      });
    });
  }

  const instancePaths = action.data.config.instancePaths
    ? action.data.config.instancePaths
    : [action.data.config.instancePath];

  store.dispatch(updateDetailsWidget(instancePaths[0]));
  const promises = [];
  for (const instancePath of instancePaths) {
    const data_path = `${instancePath}.data`;
    const data = Instances.getInstance(data_path);
    const time_path = `${instancePath}.timestamps`;
    const time = Instances.getInstance(time_path);

    if (data.getValue().resolve) {
      // Trick to resolve with the instance path instead than the type path. TODO remove when fixed
      promises.push(retrieveImportValue(time, time_path));
      promises.push(retrieveImportValue(data, data_path));
    }
  }
  if (promises.length) {
    store.dispatch(waitData("Loading timeseries data...", action.type));
    Promise.allSettled(promises).then(() => next(action));
  } else {
    next(action);
  }
}

function handleImportTimestamps (store, next, action) {
  const time_path = `${action.data.instancePath}.timestamps`;
  const timestamps = Instances.getInstance(time_path);

  if (timestamps.getValue().resolve == "ImportValue") {
    store.dispatch(waitData("Loading timestamps data...", action.type));
    timestamps.getValue().getPath = () => timestamps.getPath();

    timestamps.getValue().resolve(timeValue => {
      next(GeppettoActions.deleteInstance(timestamps)),
      Instances.getInstance(time_path);

      next(action);
    });
  } else {
    next(action);
  }
}

const nwbMiddleware = store => next => action => {
  // console.log(action);

  switch (action.type) {
  case LOAD_NWB_FILE: {
    const fileName = action.data.nwbFileUrl.match(/^http|^\//g)
      ? action.data.nwbFileUrl
      : `workspace/${action.data.nwbFileUrl}`;
    action.data.nwbFileUrl = fileName;
    next(GeppettoActions.waitData("Loading NWB file...", NWB_FILE_LOADED));
    next(action);
    next(LayoutActions.setWidgets(DEFAULT_WIDGETS));

    store.dispatch(
      GeppettoActions.loadProjectFromUrl(action.data.nwbFileUrl)
    );
    break;
  }

  case UNLOAD_NWB_FILE_IN_NOTEBOOK:
    next(action);
    Utils.execPythonMessage("del nwbfile");

    break;

  case NOTEBOOK_READY:
  case GeppettoActions.clientActions.JUPYTER_GEPPETTO_EXTENSION_READY:
    next(action);
    // FIXME for some reason the callback for python messages is not being always called
    Utils.execPythonMessage("from nwb_explorer.nwb_main import main");
    next(loadNWBFileInNotebook);
    nwbFileService
      .loadNWBFileInNotebook(store.getState().nwbfile.nwbFileUrl)
      .then(() => next(loadedNWBFileInNotebook));
    break;

  case UPDATE_WIDGET:
  case ADD_WIDGET:
  case ADD_PLOT_TO_EXISTING_WIDGET:
    return handleShowWidget(store, next, action);
  case GeppettoActions.backendActions.MODEL_LOADED:
    next(action);
    next(nwbFileLoaded());
    next(LayoutActions.addWidgets(fileLoadedLayout()));
    next(
      LayoutActions.updateWidget({ id: "general", config: { instancePath: "nwbfile" } })
    );
    break;
  case GeppettoActions.clientActions.ERROR_WHILE_EXEC_PYTHON_COMMAND:
    next(raiseError(action.data.response));
    next(GeppettoActions.hideSpinner());
    break;
  case GeppettoActions.clientActions.GEPPETTO_ERROR:
    next(raiseError(action.data.message));
    next(GeppettoActions.hideSpinner());
    break;
  default:
    next(action);
  }
};

export default nwbMiddleware;
