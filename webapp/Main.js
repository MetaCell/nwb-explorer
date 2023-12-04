
global.GEPPETTO_CONFIGURATION = require('./GeppettoConfiguration.json');
const { initGeppetto } = require('@metacell/geppetto-meta-client/GEPPETTO');
import { LoadingSpinner } from '@metacell/geppetto-meta-client/components';
import ErrorDialog from './components/reduxconnect/ErrorDialogContainer';
require('babel-polyfill');
const { Provider } = require('react-redux');
const configureStore = require('./redux/store').default;

const ReactDOM = require('react-dom');
const React = require('react');
const { MuiThemeProvider } = require('@material-ui/core/styles');

const Utils = require('./Utils').default;

const App = require('./components/reduxconnect/AppContainer').default;

// The service is also called from the parent frame to change file
const nwbFileService = require('./services/NWBFileService').default;
import { loadNWBFile, clearModel } from './redux/actions/nwbfile';

initGeppetto(true);
// MUI theming
const theme = require('./theme').default;

window.updateFile = nwbFileService.setNWBFileUrl;


const store = configureStore();


(function init () {
  
  // GEPPETTO.G.debug(true); // Change this to true to see messages on the Geppetto console while loading
  GEPPETTO.Resources.COLORS.DEFAULT = '#008ea0';
  // GEPPETTO.Manager = nwbManager; // Override standard Geppetto manager
  console.log(Utils);

  if (window !== window.parent) {
    window.parent.postMessage({ type: 'APP_READY' }, '*');
  }

  if (nwbFileService.getNWBFileUrl()) {
    store.dispatch(loadNWBFile(nwbFileService.getNWBFileUrl()));
  }

  const loadFromEvent = event => {
    // console.debug('Parent frame message received:', event)

    // Here we would expect some cross-origin check, but we don't do anything more than load a nwb file here
    switch (event.data.type) {
    case 'LOAD_RESOURCE':
      if (store.getState().nwbfile.model) {
        store.dispatch(clearModel());
      }
      store.dispatch(loadNWBFile(event.data.payload));
      break;
    case 'NO_RESOURCE': {
      this.setState({ waitFile: false });
    }
    }
  };
  // A message from the parent frame can specify the file to load
  window.addEventListener('message', loadFromEvent);

  window.load = loadFromEvent;


  ReactDOM.render(
    <MuiThemeProvider theme={theme}>
      <Provider store={store}>
        <App />
        <LoadingSpinner />
        <ErrorDialog />
      </Provider>
    </MuiThemeProvider>,
    document.getElementById('mainContainer'),
  );
}());
