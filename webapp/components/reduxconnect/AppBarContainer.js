import { connect } from 'react-redux';
import Appbar from '../AppBar';
import { unloadNWBFile, unloadNWBFileInNotebook } from '../../actions/nwbfile';
import { unloadNotebook } from '../../actions/notebook';
import { showPlot, resetLayout, showList, showAcquisition, showStimulus } from '../../actions/flexlayout';

const mapStateToProps = state => ({ embedded: state.general.embedded });

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
  showStimulus: () => dispatch(showStimulus)
});

export default connect(mapStateToProps, mapDispatchToProps)(Appbar);