import React from 'react';
import listMenuConfig from './configuration/listMenuConfiguration';
import Menu from "@geppettoengine/geppetto-ui//menu/Menu";
import { addToPlot } from '../actions/flexlayout';
const DEFAULT_MODEL_SETTINGS = { color: 'white' };

export default class ListMenuComponent extends React.Component {

  constructor (props) {
    super(props);
    this.state = { anchorEl: null, subMenu: null };
    this.showPlot = this.props.showPlot ? this.props.showPlot : () => console.debug('showPlot not defined in ' + typeof this);
    this.addToPlot = props.addToPlot ? props.addToPlot : () => console.debug('addToPlot not defined in ' + typeof this);
    this.showImageSeries = props.showImg ? props.showImg : () => console.debug('showImg not defined in ' + typeof this);
    this.showNWBWidget = props.showNWBWidget ? props.showNWBWidget : () => console.debug('showNWBWidget not defined in ' + typeof this);
    this.updateDetailsWidget = this.props.updateDetailsWidget ? this.props.updateDetailsWidget : () => console.debug('updateDetailsWidget not defined in ' + typeof this);
    this.plotAllInstances = this.plotAllInstances.bind(this);
    this.plotAll = this.props.plotAll ? this.props.plotAll : () => console.debug('plotAll not defined in ' + typeof this);
    this.goOnlyToTimeseriesWidgets = this.goOnlyToTimeseriesWidgets.bind(this);
    this.dontGoToSameHostTwice = this.dontGoToSameHostTwice.bind(this);
  }
  getModelSettings (path) {
    return this.modelSettings[path] ? this.modelSettings[path] : DEFAULT_MODEL_SETTINGS;
  }

  getDescription (nwbObjectPath) {
    let description_instance = Instances.getInstance(nwbObjectPath + '.description');
    return description_instance ? description_instance.getValue().wrappedObj.value.text : '-';
  }

  mapModelPathToList (path) {
    const instance = Instances.getInstance(path);
    let description;
    let type;
    try {
      description = this.getDescription(path)
    } catch (Error) {
      description = "Not yet supported.";
      console.debug('Description error');
    }

    try {
      type = instance.getType().getName();
    } catch (Error) {
      type = '(Unsupported)';
      console.debug('Type error');
    }

    return {
      path,
      type: type,
      description: description ? description : '-',
      ...this.getModelSettings(path)
    }
  }

  clickShowPlot ({ path, color, title }) {
    /*
     * this.modelSettings[path] = { color: color };
     * this.setState({ update: this.state.update + 1 });
     */
    Instances.getInstance(path).color = color; // TODO move to redux
    this.showPlot({ path, color, title });
  }

  addColor ({ path }) {
    /*
     * this.modelSettings[path] = { color: color };
     * this.setState({ update: this.state.update + 1 });
     */
    Instances.getInstance(path).color = "red"; // TODO move to redux
    // this.showPlot({ path, color, title });
  }

  clickShowNWBWidget ({ path }) {
    this.showNWBWidget(path);
  }

  clickShowImg ({ path }) {
    this.showImageSeries({ path });
  }

  clickShowDetails ({ path }) {
    this.updateDetailsWidget(path)
  }

  clickAddToPlot (props) {
    this.addToPlot(props)
  }

  plotAllInstances () {
    const instances = this.getInstances();

    this.plotAll({
      plots : instances.filter(instance => Instances.getInstance(`${instance.path}.data`)).map(instance => instance.path),
      title : "All plots: " + instances[0].path.split('.')[1] + (this.state.searchText ? `- ${this.state.searchText}` : '')
    } );
  }

  clickAddToWidget (selectedPlot) {

    const { instancePath, action } = this.props;
    action({
      hostId: selectedPlot.id,
      instancePath,
      type: "timeseries",
    });
    this.setState({ anchorEl: null });
  }

  dontGoToSameHostTwice (widget) {
    const { instancePaths } = widget;

    return instancePaths && instancePaths.indexOf(this.props.entity.path) == -1;
  }

  goOnlyToTimeseriesWidgets (widget) {
    const { path } = this.props.entity;
    return widget.instancePath != path;
  }

  getAvailablePlots () {
    const availablePlots = this.props.widgets
      .filter(this.goOnlyToTimeseriesWidgets)
      .filter(this.dontGoToSameHostTwice);
    let menuItems = ""
    if (availablePlots.length > 0) {
      menuItems = availablePlots.map(availablePlot =>
        ({
          label: `${availablePlot.name}`,
          action: {
            handlerAction: "redux",
            parameters: [addToPlot, {
              hostId: availablePlot.id,
              instancePath: this.props.entity.path,
              type: "timeseries",
            }],
          },
        }))

    }
    return menuItems;
  }

  menuHandler (click) {
    if (!click) {
      return;
    }
    switch (click.handlerAction) {
    case "redux": {
      const [action, payload] = click.parameters;
      if (payload !== undefined) {
        this.props.dispatchAction(action(payload));
      } else {
        this.props.dispatchAction(action);
      }

      break;
    }
    case "details": {
      this.clickShowDetails(this.props.entity)
      break;
    }
    case "plot": {
      this.clickShowPlot(this.props.entity)
      break;
    }
    case "color": {
      this.addColor(this.props.entity)
      break;
    }

    case "menuInjector": {
      const [menuName] = click.parameters;
      if (menuName === "View") {
        return this.getAvailablePlots()
      }
      break;
    }

    default:
      console.log("Menu action not mapped, it is " + click);
    }
  }

  render () {
    return <Menu
      configuration={listMenuConfig}
      menuHandler={this.menuHandler.bind(this)}
    />
  }
}