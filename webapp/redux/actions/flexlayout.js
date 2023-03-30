import { WidgetStatus, FILEVARIABLE_LENGTH } from "../../constants";

import * as LayoutActions from "@metacell/geppetto-meta-client/common/layout/actions";

export const {
  ADD_WIDGET,
  ADD_PLOT_TO_EXISTING_WIDGET,
  UPDATE_WIDGET,
  SET_LAYOUT,
  DESTROY_WIDGET,
  ACTIVATE_WIDGET,
  RESET_LAYOUT
} = LayoutActions.layoutActions;

export const showPlot = ({ path, title }) => ({
  type: ADD_WIDGET,
  data: {
    id: `plot@${path}`,
    config: { instancePaths: [path] },

    component: "Plot",
    type: "TimeSeries",
    name: title || path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: "bottomPanel"
  }
});

export const addToPlot = ({ hostId, instancePath }) => ({
  type: ADD_PLOT_TO_EXISTING_WIDGET,
  data: {
    hostId,
    config: { instancePath },
    type: "TimeSeries"
  }
});

export const plotAll = ({ plots, title }) => ({
  type: ADD_WIDGET,
  data: {
    id: `plot@${plots.join("-")}`,

    component: "Plot",
    type: "TimeSeries",
    name: title,
    status: WidgetStatus.ACTIVE,
    panelName: "bottomPanel",
    config: { instancePaths: plots }
  }
});

export const showImageSeries = ({ path, showDetail }) => ({
  type: ADD_WIDGET,
  data: {
    id: `img@${path}`,

    component: "ImageSeries",
    type: "ImageSeries",
    name: path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: "bottomPanel",
    config: { showDetail, instancePath: path }
  }
});

export const showList = (
  name,
  pathPattern,
  typePattern,
  status = WidgetStatus.ACTIVE
) => ({
  type: ADD_WIDGET,
  data: {
    id: `list@${pathPattern}`,
    config: {
      pathPattern:
        pathPattern instanceof RegExp ? pathPattern.source : pathPattern,
      typePattern:
        typePattern instanceof RegExp ? typePattern.source : typePattern
    },
    component: "ListViewer",
    name,
    status,
    panelName: "rightTop"
  }
});

export const showAcquisition = showList(
  "Acquisition",
  "^nwbfile\\.acquisition\\.",
  /Series$/
);

export const showStimulus = showList(
  "Stimulus",
  "^nwbfile\\.stimulus\\.",
  /Series$/,
  WidgetStatus.HIDDEN
);

export const showProcessing = showList(
  "Processing",
  "^nwbfile\\.processing\\.",
  /Series$/,
  WidgetStatus.HIDDEN
);

export const showSweeps = {
  type: ADD_WIDGET,
  data: {
    id: "sweep_table",
    component: "SweepTable",
    name: "Sweeps",
    status: WidgetStatus.HIDDEN,
    panelName: "rightTop"
  }
};

export const showGeneral = {
  type: ADD_WIDGET,
  data: {
    id: "general",
    name: "General",
    status: WidgetStatus.ACTIVE,
    config: { instancePath: "nwbfile" },
    component: "Metadata",
    panelName: "leftPanel",
    enableClose: false
  }
};

export const newWidget = ({ path, component, panelName }) => ({
  type: ADD_WIDGET,
  data: {
    id: path,
    instancePath: path,
    component,
    name: path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName
  }
});

export const showNWBWidget = path =>
  newWidget({ path, component: "NWBWidget", panelName: "bottomPanel" });

export const updateWidget = newConf => ({
  type: UPDATE_WIDGET,
  data: newConf
});

export const minimizeWidget = id => ({
  type: UPDATE_WIDGET,
  data: {
    id,
    status: WidgetStatus.MINIMIZED
  }
});

export const maximizeWidget = id => ({
  type: UPDATE_WIDGET,

  data: {
    id,
    status: WidgetStatus.MAXIMIZED
  }
});

export const activateWidget = id => ({
  type: ACTIVATE_WIDGET,
  data: { id }
});

export const updateDetailsWidget = path => ({
  type: ADD_WIDGET,

  data: {
    id: "details",
    name: "Details",
    config: { instancePath: path },
    status: WidgetStatus.ACTIVE,
    component: "Metadata",
    panelName: "leftPanel",
    enableClose: false,
    showObjectInfo: true
  }
});

export const destroyWidget = id => ({
  type: DESTROY_WIDGET,
  data: { id }
});

export const resetLayout = { type: RESET_LAYOUT };
