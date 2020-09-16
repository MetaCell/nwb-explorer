import { 
  ADD_WIDGET,
  UPDATE_WIDGET,
  RESET_LAYOUT,
  DESTROY_WIDGET,
  ACTIVATE_WIDGET,
  ADD_PLOT_TO_EXISTING_WIDGET,
  showList, showAcquisition, showStimulus, showSweeps, showGeneral
} from '../actions/flexlayout';

import { NWB_FILE_LOADED } from '../actions/nwbfile'

import { WidgetStatus } from '../components/constants';


function removeUndefined (obj) {
  return Object.keys(obj).forEach(key => obj[key] === undefined ? delete obj[key] : '');
}

export const FLEXLAYOUT_DEFAULT_STATUS = { 
  widgets: {
    
    'python': { 
      id: 'python', 
      name: 'Python', 
      status: WidgetStatus.MINIMIZED, 
      icon: 'fa-python',
      component: 'PythonConsole', 
      panelName: "bottomPanel",
      enableClose: false
    },
    'general': { 
      id: 'general', 
      name: 'General', 
      status: WidgetStatus.ACTIVE, 
      panelName: "leftPanel",
      enableClose: false
    },

    'details': {
      id: 'details',
      name: 'Details',
      instancePath: '',
      status: WidgetStatus.HIDDEN,
      component: 'Metadata',
      panelName: "leftPanel",
      enableClose: false,
      showObjectInfo: true
    }

    
  },

};


export default (state = FLEXLAYOUT_DEFAULT_STATUS, action) => {
  if (action.data) {
    removeUndefined(action.data); // Prevent deletion in case of unpolished update action
  }
  
  switch (action.type) {
    
  case ADD_WIDGET:
  case UPDATE_WIDGET: { 
    const newWidget = { ...state.widgets[action.data.id], panelName: extractPanelName(action), ...action.data };
    return {
      ...state, widgets: { 
        ...updateWidgetStatus(state.widgets, newWidget), 
        [action.data.id]: newWidget 
      }
    } ;
  }

  case DESTROY_WIDGET:{
    const newWidgets = { ...state.widgets };
    delete newWidgets[action.data.id];
    return { ...state, widgets: newWidgets };
  }

  case ACTIVATE_WIDGET: { 
    const activatedWidget = state.widgets[action.data.id];
    if (state.widgets['details'].panelName == activatedWidget.panelName) {
      return state;
    }
    const newDetails = activatedWidget.instancePath
      ? {
        ...state.widgets['details'], 
        instancePath: state.widgets[action.data.id].instancePath 
      } : state.widgets['details']; // We always show the meta data of currently selected widget
    return {
      ...state, widgets: { 
        ...updateWidgetStatus(state.widgets, { panelName: state.widgets[action.data.id], status: WidgetStatus.ACTIVE }), 
        details: newDetails,
        [action.data.id]: { ...activatedWidget, status: WidgetStatus.ACTIVE }
      }
    }
  }

  case RESET_LAYOUT:
    return FLEXLAYOUT_DEFAULT_STATUS;
  
  case ADD_PLOT_TO_EXISTING_WIDGET: {
    const widget = { ...state.widgets[action.data.hostId] };
    const widgets = { ...state.widgets };
    delete widgets[action.data.hostId];

    widget.instancePaths.push(action.data.instancePath);
    const newId = 'plot@' + widget.instancePaths.join('-');
    if (widget){
      return {
        widgets: { 
          ...updateWidgetStatus(widgets, { panelName: widget.panelName, status: WidgetStatus.ACTIVE }), 
          [newId]: { 
            ...widget,
            id: newId,
            name: widget.name + '+',
          } 
        } 
      }
    }
    
    
    return state
  }

  case NWB_FILE_LOADED:
    return { widgets: { ...state.widgets, ...fileLoadedLayout() } };

  default:
    return state
  }
}

function filterWidgets (widgets, filterFn) {
  return Object.fromEntries(Object.values(widgets).filter(filterFn));
}

/**
 * Ensure there is one only active widget in the same panel
 * @param {*} widgets 
 * @param {*} param1 
 */
function updateWidgetStatus (widgets, { status, panelName }) {
  if (status != WidgetStatus.ACTIVE) {
    return widgets;
  }
  return Object.fromEntries(Object.values(widgets).filter(widget => widget).map(widget => [
    widget.id,
    {
      ...widget,
      status: widget.panelName == panelName ? WidgetStatus.HIDDEN : widget.status
    }
  ]));
}

function extractPanelName (action) {
  return action.data.component == "Plot" ? "bottomPanel" : "leftPanel";
}


function fileLoadedLayout () {
  const widgets = { [showGeneral.data.id]: showGeneral.data };

  if (Instances.getInstance('nwbfile.stimulus') && Instances.getInstance('nwbfile.stimulus').getType().getVariables().length) {
    widgets[showStimulus.data.id] = showStimulus.data;
  }

  if (Instances.getInstance('nwbfile.acquisition')) {
    widgets[showAcquisition.data.id] = showAcquisition.data;
  }

  if (Instances.getInstance('nwbfile.sweep_table')) {
    widgets[showSweeps.data.id] = showSweeps.data;
  }
  return widgets;
}
    