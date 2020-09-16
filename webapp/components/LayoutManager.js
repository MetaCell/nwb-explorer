import React, { Component } from 'react';
import * as FlexLayout from '@geppettoengine/geppetto-ui/flex-layout/src/index';
import Actions from '@geppettoengine/geppetto-ui/flex-layout/src/model/Actions';


import { WidgetStatus } from './constants';
import { isEqual } from '../Utils';
import WidgetFactory from './WidgetFactory';


const defaultLayoutConfiguration = {
  "global": { sideBorders: 8 },
  "layout": {
    "type": "row",
    "weight": 100,
    "id": "root",
    "children": [
      {
        "type": "row",
        "weight": 20,
        "children": [
          {
            "type": "tabset",
            "weight": 100,
            "id": "leftPanel",
            "enableDeleteWhenEmpty": false,
            "enableDrop": false,
            "enableDrag": false,
            "enableDivide": false,
            "enableMaximize": false,
            "children": [
            
            ]
          }
        ]
      },
      {
        "type": "row",
        "weight": 80,
        "children": [
          {
            "type": "tabset",
            "weight": 50,
            "id": "bottomPanel",
            "enableDeleteWhenEmpty": false,
            "children": [
            ]
          }
        ]
      }
    ]
  },
  "borders": [
    {
      "type": "border",
      "location": "bottom",
      "size": 100,
      "children": [],
      "barSize": 10
    }
  ]
};

/**
 * Transforms a widget configutation into a flexlayout node descriptor
 */
function widget2Node (configuration) {
  const { id, name, component, instancePath, status, panelName, enableClose = true } = configuration;
  return {
    id,
    name,
    status,
    component,
    type: "tab",
    enableRename: false,
    enableClose: enableClose,
    // attr defined inside config, will also be available from within flexlayout nodes.  For example:  node.getNodeById(id).getConfig()
    config: configuration ,
  };
}

export default class LayoutManager extends Component {

  constructor (props) {
    super(props);
    const layout = this.props.layout ? this.props.layout : defaultLayoutConfiguration;
    this.model = FlexLayout.Model.fromJson(layout);
    this.destroyWidget = this.props.destroyWidget ? this.props.destroyWidget : () => console.debug('destroyWidget not defined');
    this.activateWidget = this.props.activateWidget ? this.props.activateWidget : () => console.debug('activateWidget not defined');
    this.maximizeWidget = this.props.maximizeWidget ? this.props.maximizeWidget : () => console.debug('maximizeWidget not defined');
    this.minimizeWidget = this.props.minimizeWidget ? this.props.minimizeWidget : () => console.debug('minimizeWidget not defined');
    

    this.widgetFactory = this.props.widgetFactory ? this.props.widgetFactory : new WidgetFactory();
  }
  componentDidMount () {
    const { widgets } = this.props;
    this.addWidgets(Object.values(widgets));
  }

  componentDidUpdate (prevProps, prevState) {
    const { widgets } = this.props;
    const oldWidgets = prevProps.widgets;
    const newWidgets = this.findNewWidgets(widgets, oldWidgets);
    if (newWidgets) {
      this.addWidgets(newWidgets);
    }
    
    const updatedWidgets = this.findUpdatedWidgets(widgets, oldWidgets);
    if (updatedWidgets) {
      this.updateWidgets(updatedWidgets);
    }

    const deletedWidgets = this.findDeletedWidgets(widgets, oldWidgets);

    if (deletedWidgets) {
      this.deleteWidgets(deletedWidgets);
    }
  }
 
  addWidgets (widgets) {
    const { model } = this;
    for (let newWidgetDescriptor of widgets) {

      if (!model.getNodeById(newWidgetDescriptor.id)) {
        this.addWidget(newWidgetDescriptor);
      } else {
        console.warn('Should not be here in addWidgets...');
      }
      
    }
    for (let widget of widgets) {
   
      if (widget.status == WidgetStatus.ACTIVE) {
        this.model.doAction(FlexLayout.Actions.selectTab(widget.id));
      }
      
    }
    // window.dispatchEvent(new Event('resize'));
  }

  deleteWidgets (widgets) {
    for (let widget of widgets) {
      this.model.doAction(FlexLayout.Actions.deleteTab(widget.id));
    }
  }

  addWidget (widgetConfiguration) {
    this.refs.layout.addTabToTabSet(widgetConfiguration.panelName, widget2Node(widgetConfiguration));
  }

  updateWidgets (widgets) {

    for (let widget of widgets) {

      this.updateWidget(widget);
   
      // This updates plotly.js plots to new panel sizes
      if (widget.status == WidgetStatus.ACTIVE) {
        this.model.doAction(FlexLayout.Actions.selectTab(widget.id));
      }
      
    }
    // window.dispatchEvent(new Event('resize'));
  }

  updateWidget (widget) {
    if (widget) {
      this.widgetFactory.updateWidget(widget);
      this.model.doAction(Actions.updateNodeAttributes(widget.id, widget2Node(widget))); 
    }
    
  }

  
  factory (node) {
    return this.widgetFactory.factory(node.getConfig());
  }


  findNewWidgets (widgets, oldWidgets) {
    return oldWidgets ? Object.values(widgets).filter(widget => widget && !oldWidgets[widget.id]) : Object.values(widgets);
  }

  findUpdatedWidgets (widgets, oldWidgets) {
    return oldWidgets 
      ? Object.values(widgets)
        .filter(widget => widget && oldWidgets[widget.id] && !isEqual(widget, oldWidgets[widget.id])) 
      : Object.values(widgets);
  }

  findDeletedWidgets (widgets, oldWidgets) {
    return oldWidgets ? Object.values(oldWidgets).filter(widget => widget && !widgets[widget.id]) : Object.values(widgets);
  }
  

  onAction (action) {
    switch (action.type){
    case Actions.SET_ACTIVE_TABSET:
      break;
    case Actions.SELECT_TAB: 
      this.activateWidget(action.data.tabNode);
      window.dispatchEvent(new Event('resize'));
      break;
    case Actions.DELETE_TAB:
      this.onActionDeleteWidget(action);
      window.dispatchEvent(new Event('resize'));
      break;
    case Actions.MAXIMIZE_TOGGLE:
      this.onActionMaximizeWidget(action);
      window.dispatchEvent(new Event('resize'));
      break;
    case Actions.ADJUST_SPLIT:
    case Actions.MOVE_NODE :
      window.dispatchEvent(new Event('resize'));
      break;
    }
       
    this.model.doAction(action);
  }

  onActionMaximizeWidget (action) {
    const { model } = this;
    const { widgets } = this.props;
    const { maximizeWidget, activateWidget } = this;
    const panel2maximize = model.getNodeById(action.data.node);
    
    if (panel2maximize.getChildren().length > 0) {
      const widgetId2maximize = panel2maximize.getSelectedNode().getId();
      const maximizedWidget = this.findMaximizedWidget(widgets);
      if (maximizedWidget) {
        if (maximizedWidget.id !== widgetId2maximize) {
          maximizeWidget(widgetId2maximize);
        }
        activateWidget(maximizedWidget.id);
      
      } else {
        maximizeWidget(widgetId2maximize);
      }
    }
    
  }

  findMaximizedWidget (widgets) {
    return Object.values(widgets).find(widget => widget && widget.status == WidgetStatus.MAXIMIZED);
  }

  onActionDeleteWidget (action) {
    const { model } = this;
    const { widgets } = this.props;
    const maximizedWidget = this.findMaximizedWidget(widgets);
    // change widget status
    this.destroyWidget(action.data.node);
    // check if the current maximized widget is the same than in the action dispatched
    if (maximizedWidget && maximizedWidget.id == action.data.node) {
      // find if there exists another widget in the maximized panel that could take its place
      const panelChildren = model.getActiveTabset().getChildren();
      const index = panelChildren.findIndex(child => child.getId() == action.data.node);
      // Understand if the tab to the left or right of the destroyed tab will be the next one to be maximized
      if (index != -1 && panelChildren.length > 1) {
        if (index == 0) {
          this.onActionMaximizeWidget(panelChildren[1].getId());
        } else {
          this.onActionMaximizeWidget(panelChildren[index - 1].getId());
        }
      }
    }
  }


  clickOnBordersAction (node) {
    this.model.doAction(FlexLayout.Actions.moveNode(node.getId(), 'bottomPanel', FlexLayout.DockLocation.CENTER, 0));
  }

  onRenderTabSet (panel, renderValues) {
    if (panel.getType() === "tabset") {
      if (panel.getId() != 'leftPanel' && panel.getChildren().length > 0){
        renderValues.buttons.push(<div key={panel.getId()} className="fa fa-window-minimize customIconFlexLayout" onClick={() => {
          this.model.doAction(FlexLayout.Actions.moveNode(panel.getSelectedNode().getId(), "border_bottom", FlexLayout.DockLocation.CENTER, 0));
        }} />);
      }
    }
  }
  
  render () {
    
    return (
      <FlexLayout.Layout
        ref="layout"
        model={this.model}
        factory={this.factory.bind(this)}
        onAction={action => this.onAction(action)}
        clickOnBordersAction={node => this.clickOnBordersAction(node)}
        onRenderTabSet={(node, renderValues) => this.onRenderTabSet(node, renderValues)}
      />
    )
  }
}