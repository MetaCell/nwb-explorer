import { connect } from 'react-redux';
import AddPlotMenu from '../AddPlotMenu';

const mapStateToProps = (state, ownProps) => ({ 
  icon: ownProps.icon,
  widgets: state.flexlayout.widgets
});

export default connect(mapStateToProps)(AddPlotMenu)