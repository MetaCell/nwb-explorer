import { connect } from 'react-redux';
import SweepTableViewer from '../SweepTableViewer';
import { showPlot, showImageSeries, updateDetailsWidget, addToPlot, showNWBWidget, plotAll, } from '../../redux/actions/widgets';

const mapStateToProps = state => ({ modelSettings: state.nwbfile.modelSettings });

const mapDispatchToProps = dispatch => ({
  showPlot: instanceDescriptor => dispatch(showPlot(instanceDescriptor)),
  showImg: instanceDescriptor => dispatch(showImageSeries(instanceDescriptor)),
  addToPlot: instanceDescriptor => dispatch(addToPlot(instanceDescriptor)),
  updateDetailsWidget: path => dispatch(updateDetailsWidget(path)),
  plotAll: instanceDescriptor => dispatch(plotAll(instanceDescriptor)),
  showNWBWidget: path => dispatch(showNWBWidget(path)),
});

export default connect(mapStateToProps, mapDispatchToProps)(SweepTableViewer);
