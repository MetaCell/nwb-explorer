
global.GEPPETTO_CONFIGURATION = require('./GeppettoConfiguration.json');
const { initGeppetto } = require('@metacell/geppetto-meta-client/GEPPETTO');
import { LoadingSpinner } from '@metacell/geppetto-meta-client/components';
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
const nwbManager = require('./services/NWBGeppettoManager').default;
initGeppetto();
// MUI theming
const theme = require('./theme').default;

window.updateFile = nwbFileService.setNWBFileUrl;

// G.enableLocalStorage(false);
// G.setIdleTimeOut(-1);

const store = configureStore();

(function init () {
  
  // GEPPETTO.G.debug(true); // Change this to true to see messages on the Geppetto console while loading
  GEPPETTO.Resources.COLORS.DEFAULT = '#008ea0';
  // GEPPETTO.Manager = nwbManager; // Override standard Geppetto manager
  console.log(Utils);

  ReactDOM.render(
    <MuiThemeProvider theme={theme}>
      <Provider store={store}>
        <App />
        <LoadingSpinner />
      </Provider>
    </MuiThemeProvider>,
    document.getElementById('mainContainer'),
  );
}());
