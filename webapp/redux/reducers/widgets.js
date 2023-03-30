import {
  ADD_WIDGET,
  UPDATE_WIDGET,
  RESET_LAYOUT,
  DESTROY_WIDGET,
  ACTIVATE_WIDGET,
  ADD_PLOT_TO_EXISTING_WIDGET,
  showList, showAcquisition, showStimulus, showProcessing, showSweeps, showGeneral,
} from '../actions/flexlayout';

import { NWB_FILE_LOADED } from '../actions/nwbfile';

import { WidgetStatus } from '../../constants';

function removeUndefined (obj) {
  return Object.keys(obj).forEach(key => (obj[key] === undefined ? delete obj[key] : ''));
}

export const DEFAULT_WIDGETS = {
  python: {
    id: "python",
    name: "Python",
    status: WidgetStatus.MINIMIZED,
    icon: "fa-python",
    component: "PythonConsole",
    panelName: "bottomPanel",
    enableClose: false,
  },
  general: {
    id: "general",
    name: "General",
    status: WidgetStatus.ACTIVE,
    component: "placeholder",
    panelName: "leftPanel",
    enableClose: false
  },
  details: {
    id: "details",
    name: "Details",
    config: { instancePath: "" },
    status: WidgetStatus.HIDDEN,
    component: "Metadata",
    panelName: "leftPanel",
    enableClose: false,
    showObjectInfo: true
  }
};


export default (state = {}, action) => {
  if (action.data) {
    removeUndefined(action.data); // Prevent deletion in case of unpolished update action
  }

  switch (action.type) {
  

  case RESET_LAYOUT:
    return DEFAULT_WIDGETS;

  case ADD_PLOT_TO_EXISTING_WIDGET: {
    const widget = { ...state.widgets[action.data.hostId] };
    const widgets = { ...state.widgets };
    delete widgets[action.data.hostId];

    widget.instancePaths.push(action.data.instancePath);
    const newId = `plot@${widget.instancePaths.join('-')}`;
    if (widget) {
      return {
        widgets: {
          ...updateWidgetStatus(widgets, { panelName: widget.panelName, status: WidgetStatus.ACTIVE }),
          [newId]: {
            ...widget,
            id: newId,
            name: `${widget.name}+`,
          },
        },
      };
    }

    return state;
  }


  default:
    return state;
  }
};

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
      status: widget.panelName == panelName ? WidgetStatus.HIDDEN : widget.status,
    },
  ]));
}

function extractPanelName (action) {
  return action.data.component == 'Plot' ? 'bottomPanel' : 'leftPanel';
}

