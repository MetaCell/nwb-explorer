import App from '../App';
import { connect } from "react-redux";
import { loadNWBFile, nwbFileLoaded, unloadNWBFileInNotebook, unloadNWBFile, resetLayout } from '../../actions/nwbfile';
import { notebookReady, loadNotebook } from '../../actions/notebook';
import { raiseError } from '../../actions/general'


const mapStateToProps = state => ({
  ...state.nwbfile,
  ...state.general,
  ...state.notebook
});

const mapDispatchToProps = dispatch => ({
  loadNotebook: () => dispatch(loadNotebook),
  reset: () => {
    dispatch(unloadNWBFileInNotebook());
    dispatch(unloadNWBFile);
    dispatch(resetLayout);
  },
  notebookReady: () => dispatch(notebookReady),
  nwbFileLoaded: model => dispatch(nwbFileLoaded(model)),
  loadNWBFile: nwbFileUrl => dispatch(loadNWBFile(nwbFileUrl)),
  raiseError: error => dispatch(raiseError(error))
});

export default connect(mapStateToProps, mapDispatchToProps)(App);