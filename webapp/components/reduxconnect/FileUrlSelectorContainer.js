import { connect } from 'react-redux';
import FileUrlSelector from '../FileUrlSelector';

import { loadNWBFile } from '../../redux/actions/nwbfile';


FileUrlSelector.defaultProps = {};

const mapStateToProps = state => ({});
const mapDispatchToProps = dispatch => ({ loadNWBFile: filePath => dispatch(loadNWBFile(filePath)) });

export default connect(mapStateToProps, mapDispatchToProps)(FileUrlSelector);
