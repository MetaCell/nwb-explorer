import { connect } from 'react-redux';
import AddPlotMenu from '../AddPlotMenu';

const mapStateToProps = (state, ownProps) => ({ 
  icon: ownProps.icon,
  widgets: Object.values(state.flexlayout.widgets).filter(w => w.component == "Plot").map(w => ({ instancePaths: w.instancePaths, id: w.id, name: w.name }))
});

export default connect(mapStateToProps)(AddPlotMenu);