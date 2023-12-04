import { connect } from 'react-redux';
import NWBPlot from '../NWBPlot';

const mapStateToProps = state => ({ modelSettings: state.nwbfile.modelSettings });

export default connect(mapStateToProps, null)(NWBPlot);
