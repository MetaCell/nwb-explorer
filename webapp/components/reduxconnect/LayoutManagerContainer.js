import { connect } from 'react-redux';
import LayoutManager from '../LayoutManager';
import { 
  activateWidget,
  destroyWidget,
  minimizeWidget,
  maximizeWidget,
} from '../../actions/flexlayout';

const mapStateToProps = state => state.flexlayout;

const mapDispatchToProps = dispatch => ({
  minimizeWidget: id => dispatch(minimizeWidget(id)),
  destroyWidget: id => dispatch(destroyWidget(id)),
  maximizeWidget: id => dispatch(maximizeWidget(id)),
  activateWidget: id => dispatch(activateWidget(id)),
});
console.log(LayoutManager);
export default connect(mapStateToProps, mapDispatchToProps)(LayoutManager);