import { connect } from 'react-redux';
import Dialog from '../Dialog';
import { closeDialog } from '../../redux/actions/general';

const mapStateToProps = state => ({ open: state.general.dialogOpen, title: state.general.dialogTitle, message: state.general.dialogMessage });

const mapDispatchToProps = dispatch => ({ handleClose: () => dispatch(closeDialog) });

export default connect(mapStateToProps, mapDispatchToProps)(Dialog);
