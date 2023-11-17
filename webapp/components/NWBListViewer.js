import React, { Component } from 'react';
import ListViewer from '@metacell/geppetto-meta-ui/list-viewer/ListViewer';
import RemoveRedEyeIcon from '@material-ui/icons/RemoveRedEye';
import listViewerConf from './configuration/listViewerConfiguration.js';

const DEFAULT_MODEL_SETTINGS = { color: '#ffffff' };
const TYPE_INCLUDE_REGEX = /^(?!.*details)Model.nwbfile.*$/;

export default class NWBListViewer extends Component {
  constructor (props) {
    super(props);
    this.updates = 0;
    this.showPlot = this.props.showPlot ? this.props.showPlot : () => console.debug(`showPlot not defined in ${typeof this}`);
    this.addToPlot = props.addToPlot ? props.addToPlot : () => console.debug(`addToPlot not defined in ${typeof this}`);
    this.showImageSeries = props.showImg ? props.showImg : () => console.debug(`showImg not defined in ${typeof this}`);
    this.showNWBWidget = props.showNWBWidget ? props.showNWBWidget : () => console.debug(`showNWBWidget not defined in ${typeof this}`);
    this.updateDetailsWidget = this.props.updateDetailsWidget ? this.props.updateDetailsWidget : () => console.debug(`updateDetailsWidget not defined in ${typeof this}`);
    this.updateSettings = this.props.updateSettings ? this.props.updateSettings : () => console.debug(`updateSettings not defined in ${typeof this}`);
    this.plotAllInstances = this.plotAllInstances.bind(this);
    this.plotAll = this.props.plotAll ? this.props.plotAll : () => console.debug(`plotAll not defined in ${typeof this}`);
    this.state = { update: 0, searchText: '' };
    this.filter = this.props.filter ? this.props.filter.bind(this) : this.filter.bind(this);
  }

  componentDidUpdate () {
    this.updates++;
  }

  getModelSettings (path) {
    return this.props.modelSettings[path] ? this.props.modelSettings[path] : DEFAULT_MODEL_SETTINGS;
  }

  getDescription (nwbObjectPath) {
    const description_instance = Instances.getInstance(`${nwbObjectPath}.description`);
    return description_instance ? description_instance.getValue().wrappedObj.value.text : '-';
  }

  mapModelPathToList (path) {
    const instance = Instances.getInstance(path);
    let description;
    let type;
    try {
      description = this.getDescription(path);
    } catch (Error) {
      description = 'Not yet supported.';
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
      type,
      description: description || '-',
      ...this.getModelSettings(path),
    };
  }

  clickShowPlot ({ path, title }) {
    this.showPlot({ path, title });
  }

  clickShowNWBWidget ({ path }) {
    this.showNWBWidget(path);
  }

  clickShowImg ({ path }) {
    this.showImageSeries({ path, showDetail: true });
  }

  clickShowDetails ({ path }) {
    this.updateDetailsWidget(path);
  }

  clickTitleDetails (path) {
    this.updateDetailsWidget(`nwbfile.${path}`);
  }

  clickAddToPlot (props) {
    this.addToPlot(props);
  }

  plotAllInstances () {
    const instances = this.getInstances();

    this.plotAll({
      plots: instances.filter(instance => Instances.getInstance(`${instance.path}.data`)).map(instance => instance.path),
      title: `All plots: ${instances[0].path.split('.')[1]}${this.state.searchText ? `- ${this.state.searchText}` : ''}`,
    });
  }

  filter (pathObj) {
    const { path, type } = pathObj;
    const { pathPattern, typePattern } = this.props;

    if (type.match(TYPE_INCLUDE_REGEX)) {
      if (path.match(pathPattern)) {
        const instance = Instances.getInstance(path);
        if (instance.getPath) {
          return instance.getType().getName().match(typePattern)
          && (instance.getId().toLowerCase().includes(this.state.searchText.toLowerCase()) || this.getDescription(path).toLowerCase().includes(this.state.searchText.toLowerCase()));
        }
      }
    }

    return false;
  }

  onFilter (e) {
    this.setState({ searchText: e });
  }

  getInstances () {
    return GEPPETTO.ModelFactory.allPaths
      .filter(this.filter)
      .map(({ path }) => this.mapModelPathToList(path));
  }

  getColumnConfiguration () {
    return listViewerConf;
  }

  render () {
    const instances = this.getInstances();

    return (
      <div className="list-container">
        <div style={{ flex: 1, overflow: 'auto' }}>
          <ListViewer
            columnConfiguration={this.getColumnConfiguration()}
            instances={instances}
            handler={this}
            infiniteScroll
            update={this.state.update}
            events={{ onFilter: filteredText => this.onFilter(filteredText) }}
          />
        </div>

        <div className="list-summary">
          <a title="Plot all timeseries" onClick={this.plotAllInstances}>
            <RemoveRedEyeIcon />
          </a>
          { instances.length > 0
            ? (
              <i>
                {instances.length}
                {' '}
                Matching Results
              </i>
            )
            : null}
        </div>
      </div>
    );
  }
}
