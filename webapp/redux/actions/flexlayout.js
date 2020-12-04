import { WidgetStatus, FILEVARIABLE_LENGTH } from '../../constants';

export const UPDATE_WIDGET = 'UPDATE_WIDGET';
export const ACTIVATE_WIDGET = 'ACTIVATE_WIDGET';
export const ADD_WIDGET = 'ADD_WIDGET';
export const RESET_LAYOUT = 'RESET_LAYOUT';
export const DESTROY_WIDGET = 'DESTROY_WIDGET';
export const ADD_PLOT_TO_EXISTING_WIDGET = 'ADD_PLOT_TO_EXISTING_WIDGET'

export const showPlot = ({ path, title }) => ({
  type: ADD_WIDGET,
  data: {
    id: 'plot@' + path,
    instancePaths: [path],
    component: 'Plot',
    type: 'TimeSeries',
    name: title ? title : path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: 'bottomPanel',
    config: {}
  }
});

export const addToPlot = ({ hostId, instancePath }) => ({
  type: ADD_PLOT_TO_EXISTING_WIDGET,
  data: {
    hostId,
    instancePath,
    type: 'TimeSeries'
  }
});


export const plotAll = ({ plots, title }) => ({
  type: ADD_WIDGET,
  data: {
    id: 'plot@' + plots.join('-'),
    instancePaths: plots,
    component: 'Plot',
    type: 'TimeSeries',
    name: title,
    status: WidgetStatus.ACTIVE,
    panelName: 'bottomPanel',
    config: {},
  }
});

export const showImageSeries = ({ path, showDetail }) => ({
  type: ADD_WIDGET,
  data: {
    id: 'img@' + path,
    instancePath: path,
    component: 'ImageSeries',
    type: 'ImageSeries',
    name: path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: 'bottomPanel',
    config: { showDetail }
  }
});


export const showList = (name, pathPattern, typePattern, status = WidgetStatus.ACTIVE) => ({
  type: ADD_WIDGET,
  data: {
    id: 'list@' + pathPattern,
    pathPattern: pathPattern instanceof RegExp ? pathPattern.source : pathPattern,
    typePattern: typePattern instanceof RegExp ? typePattern.source : typePattern,
    component: 'ListViewer',
    name: name,
    status: status,
    panelName: 'rightTop'
  }
});

export const showAcquisition = showList('Acquisition', "^nwbfile\\.acquisition\\.", /Series$/);

export const showStimulus = showList('Stimulus', "^nwbfile\\.stimulus\\.", /Series$/, WidgetStatus.HIDDEN);

export const showSweeps = {
  type: ADD_WIDGET,
  data: {
    id: 'sweep_table',
    component: 'SweepTable',
    name: 'Sweeps',
    status: WidgetStatus.HIDDEN,
    panelName: 'rightTop'
  }
}

export const showGeneral = {
  type: ADD_WIDGET,
  data: {
    id: 'general',
    name: 'General',
    status: WidgetStatus.ACTIVE,
    instancePath: 'nwbfile',
    component: 'Metadata',
    panelName: "leftPanel",
    enableClose: false
  }
}


export const newWidget = ({ path, component, panelName }) => ({
  type: ADD_WIDGET,
  data: {
    id: path,
    instancePath: path,
    component: component,
    name: path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: panelName
  }
});

export const showNWBWidget = path => (newWidget({ path, component: 'NWBWidget', panelName: 'bottomPanel' }));

export const updateWidget = (newConf => ({
  type: UPDATE_WIDGET,
  data: newConf
}))


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
    id: 'details', 
    name: 'Details', 
    instancePath: path,
    status: WidgetStatus.ACTIVE, 
    component: 'Metadata', 
    panelName: "leftPanel",
    enableClose: false,
    showObjectInfo: true
  }
});

export const destroyWidget = id => ({
  type: DESTROY_WIDGET,
  data: { id }

});

export const resetLayout = { type: RESET_LAYOUT, };

