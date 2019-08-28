import { connect } from "react-redux";
import FileUrlSelector from '../FileUrlSelector';
import { withStyles } from '@material-ui/core/styles';

import { loadNWBFile } from '../../actions/nwbfile';

const styles = () => ({ inputs: { margin: 2 } });

FileUrlSelector.defaultProps = {};

const mapStateToProps = state => ({});
const mapDispatchToProps = dispatch => ({ loadNWBFile: filePath => dispatch(loadNWBFile(filePath)) });

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(FileUrlSelector));