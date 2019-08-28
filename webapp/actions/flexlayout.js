import { WidgetStatus, FILEVARIABLE_LENGTH } from '../components/constants';

export const UPDATE_WIDGET = 'UPDATE_WIDGET';
export const ACTIVATE_WIDGET = 'ACTIVATE_WIDGET';
export const ADD_WIDGET = 'ADD_WIDGET';
export const RESET_LAYOUT = 'RESET_LAYOUT';
export const DESTROY_WIDGET = 'DESTROY_WIDGET';
export const ADD_PLOT_TO_EXISTING_WIDGET = 'ADD_PLOT_TO_EXISTING_WIDGET'

export const showPlot = ({ path, color = 'red' }) => ({ 
  type: ADD_WIDGET,
  data: {
    id: 'plot@' + path, 
    instancePath: path,
    component: 'Plot', 
    type: 'TimeSeries',
    name: path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: 'bottomPanel',
    color: color,
    config: {},
    guestList: []
  }
});

export const addToPlot = ({ hostId, instancePath, color }) => ({ 
  type: ADD_PLOT_TO_EXISTING_WIDGET,
  data: {
    hostId,
    instancePath,
    color,
    type: 'TimeSeries'
  }
});

export const showImageSeries = ({ path, type }) => ({ 
  type: ADD_WIDGET,
  data: {
    id: 'img@' + path, 
    instancePath: path,
    component: 'ImageSeries', 
    type: 'ImageSeries',
    name: path.slice(FILEVARIABLE_LENGTH),
    status: WidgetStatus.ACTIVE,
    panelName: 'bottomPanel',
    config: {}
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

export const showStimulus = showList('Stimulus', /^nwbfile\\.stimulus\\./, /Series$/, WidgetStatus.HIDDEN);

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
  type: UPDATE_WIDGET,
  data: { id: 'details', instancePath: path, showObjectInfo: true, status: WidgetStatus.ACTIVE }
});

export const destroyWidget = id => ({ 
  type: DESTROY_WIDGET,
  data: { id }
  
});

export const resetLayout = { type: RESET_LAYOUT, };

