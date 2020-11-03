import { connect } from 'react-redux';
import ErrorDialog from '../ErrorDialog';
import { RECOVER_FROM_ERROR } from '../../redux/actions/general';


const mapStateToProps = state => ({ error: state.general.error });

const mapDispatchToProps = dispatch => ({ startRecoveryFromError: () => dispatch({ type: RECOVER_FROM_ERROR }) });

export default connect(mapStateToProps, mapDispatchToProps)(ErrorDialog);
