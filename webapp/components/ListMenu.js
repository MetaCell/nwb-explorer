import React from 'react';
import Menu from '@metacell/geppetto-meta-ui//menu/Menu';
import { CompactPicker } from 'react-color';
import { listMenuConfigurations } from './configuration/listMenuConfiguration';
import { addToPlot } from '../redux/actions/flexlayout';

export default class ListMenuComponent extends React.Component {
  constructor (props) {
    super(props, null);
    this.state = { anchorEl: null, subMenu: null };
    this.showPlot = this.props.showPlot ? this.props.showPlot : () => console.debug(`showPlot not defined in ${typeof this}`);
    this.addToPlot = props.addToPlot ? props.addToPlot : () => console.debug(`addToPlot not defined in ${typeof this}`);
    this.showImageSeries = props.showImg ? props.showImg : () => console.debug(`showImg not defined in ${typeof this}`);
    this.updateDetailsWidget = this.props.updateDetailsWidget ? this.props.updateDetailsWidget : () => console.debug(`updateDetailsWidget not defined in ${typeof this}`);
    this.updateSettings = this.props.updateSettings ? this.props.updateSettings : () => console.debug(`updateSettings not defined in ${typeof this}`);
    this.goOnlyToTimeseriesWidgets = this.goOnlyToTimeseriesWidgets.bind(this);
    this.dontGoToSameHostTwice = this.dontGoToSameHostTwice.bind(this);
    this.Picker = CompactPicker;
  }

  clickShowPlot ({ path, title }) {
    this.showPlot({ path, title });
  }

  clickShowImg () {
    this.showImageSeries({ path: this.props.entity.path, showDetail: false });
  }

  clickShowDetails ({ path }) {
    this.updateDetailsWidget(path);
  }

  clickAddToPlot (props) {
    this.addToPlot(props);
  }

  dontGoToSameHostTwice (widget) {
    const { instancePaths } = widget;
    return instancePaths && instancePaths.indexOf(this.props.entity.path) == -1;
  }

  goOnlyToTimeseriesWidgets (widget) {
    const { path } = this.props.entity;
    return widget.instancePath != path;
  }

  availablePlots = () => this.props.widgets.filter(this.goOnlyToTimeseriesWidgets).filter(this.dontGoToSameHostTwice);

  getAvailablePlots () {
    const availablePlots = this.availablePlots();
    let menuItems = '';
    if (availablePlots.length > 0) {
      menuItems = availablePlots.map(availablePlot => ({
        label: `${availablePlot.name}`,
        action: {
          handlerAction: 'redux',
          parameters: [addToPlot, {
            hostId: availablePlot.id,
            instancePath: this.props.entity.path,
            type: 'timeseries',
          }],
        },
      }));
    }
    return menuItems;
  }

  handleColorChange (color) {
    this.setState({ anchorEl: null });
    const entity = {
      path: this.props.entity.path,
      color: color.hex,
    };
    this.updateSettings(entity);
  }

  getColorPicker () {
    const { color } = this.state;
    const colorPicker = React.createElement(this.Picker, {
      color,
      onChange: color => this.handleColorChange(color),
    });
    const menuItems = [{ label: colorPicker }];
    return menuItems;
  }

  menuHandler (click) {
    if (!click) {
      return;
    }
    switch (click.handlerAction) {
    case 'redux': {
      const [action, payload] = click.parameters;
      if (payload !== undefined) {
        this.props.dispatchAction(action(payload));
      } else {
        this.props.dispatchAction(action);
      }

      break;
    }
    case 'details': {
      this.clickShowDetails(this.props.entity);
      break;
    }
    case 'plot': {
      this.clickShowPlot(this.props.entity);
      break;
    }
    case 'image': {
      this.clickShowImg();
      break;
    }

    case 'menuInjector': {
      const [menuName] = click.parameters;
      if (menuName === 'AddPlot') {
        return this.getAvailablePlots();
      }
      if (menuName === 'Color') {
        return this.getColorPicker();
      }
      break;
    }

    default:
      console.log(`Menu action not mapped, it is ${click}`);
    }
  }

  render () {
    const availablePlots = this.availablePlots();
    const config = listMenuConfigurations(Instances, this.props.entity, availablePlots);
    return (
      <Menu
        configuration={config}
        menuHandler={this.menuHandler.bind(this)}
      />
    );
  }
}
