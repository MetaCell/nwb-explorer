import { connect } from 'react-redux';
import ListMenuComponent from '../ListMenu';
import { showPlot, showImageSeries, updateDetailsWidget, addToPlot } from '../../redux/actions/flexlayout';
import { updateSettings } from '../../redux/actions/nwbfile';

const mapStateToProps = state => ({
  modelSettings: state.nwbfile.modelSettings,
  widgets: Object.values(state.flexlayout.widgets).filter(w => w.component == "Plot").map(w => ({ instancePaths: w.instancePaths, id: w.id, name: w.name })),
});

const mapDispatchToProps = dispatch => ({
  showPlot: instanceDescriptor => dispatch(showPlot(instanceDescriptor)),
  showImg: instanceDescriptor => dispatch(showImageSeries(instanceDescriptor)),
  addToPlot: instanceDescriptor => dispatch(addToPlot(instanceDescriptor)),
  updateDetailsWidget: path => dispatch(updateDetailsWidget(path)),
  updateSettings: instanceDescriptor => dispatch(updateSettings(instanceDescriptor)),
  dispatchAction: action => dispatch(action)
});

export default connect(mapStateToProps, mapDispatchToProps)(ListMenuComponent);