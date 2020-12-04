import App from '../App';
import { connect } from "react-redux";
import { loadNWBFile, nwbFileLoaded, unloadNWBFileInNotebook, unloadNWBFile } from '../../redux/actions/nwbfile';
import { resetLayout } from '../../redux/actions/flexlayout';
import { notebookReady, loadNotebook } from '../../redux/actions/notebook';
import { raiseError } from '../../redux/actions/general'


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