import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import FileUrlSelector from '../FileUrlSelector';

import { loadNWBFile } from '../../redux/actions/nwbfile';

const styles = () => ({ inputs: { margin: 2 } });

FileUrlSelector.defaultProps = {};

const mapStateToProps = state => ({});
const mapDispatchToProps = dispatch => ({ loadNWBFile: filePath => dispatch(loadNWBFile(filePath)) });

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(FileUrlSelector));
