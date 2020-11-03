import { connect } from 'react-redux';
import Appbar from '../appBar/AppBar';
import { unloadNWBFile, unloadNWBFileInNotebook } from '../../redux/actions/nwbfile';
import { unloadNotebook } from '../../redux/actions/notebook';
import { showPlot, resetLayout, showList, showAcquisition, showStimulus } from '../../redux/actions/flexlayout';

const mapStateToProps = state => ({ dialogOpen: state.general.dialogOpen, embedded: state.general.embedded });

const mapDispatchToProps = dispatch => ({ 
  exit: () => {
    dispatch(unloadNWBFileInNotebook());
    dispatch(unloadNWBFile);
    dispatch(resetLayout);
    dispatch(unloadNotebook);
  },
  showPlot: instanceDescriptor => dispatch(showPlot(instanceDescriptor)),
  resetLayout: () => dispatch(resetLayout),
  showList: (name, pathPattern, typePattern) => dispatch(showList(name, pathPattern, typePattern)),
  showAcquisition: () => dispatch(showAcquisition),
  showStimulus: () => dispatch(showStimulus),
  dispatchAction: action => dispatch(action)
});

export default connect(mapStateToProps, mapDispatchToProps)(Appbar);
