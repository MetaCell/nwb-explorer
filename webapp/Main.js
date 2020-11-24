global.jQuery = require("jquery");
global.GEPPETTO_CONFIGURATION = require("./GeppettoConfiguration.json");

require("babel-polyfill");
const Provider = require("react-redux").Provider;
const configureStore = require("./redux/store").default;

require("@geppettoengine/geppetto-client-initialization");
const ReactDOM = require("react-dom");
const React = require("react");
const MuiThemeProvider = require('@material-ui/core/styles').MuiThemeProvider;

const Utils = require("./Utils").default;

const App = require("./components/reduxconnect/AppContainer").default;

// The service is also called from the parent frame to change file
const nwbFileService = require("./services/NWBFileService").default;
const nwbManager = require("./services/NWBGeppettoManager").default;

// MUI theming
const theme = require('./theme').default

window.updateFile = nwbFileService.setNWBFileUrl;


G.enableLocalStorage(false);
G.setIdleTimeOut(-1);

const store = configureStore();

(function init () {
  GEPPETTO.G.setIdleTimeOut(-1);
  GEPPETTO.G.debug(true); // Change this to true to see messages on the Geppetto console while loading
  GEPPETTO.Resources.COLORS.DEFAULT = "#008ea0";
  GEPPETTO.Manager = nwbManager; // Override standard Geppetto manager
  console.log(Utils);

  ReactDOM.render(
    <MuiThemeProvider theme={theme}>
      <Provider store={store}>
        <App />
      </Provider>
    </MuiThemeProvider>,
    document.getElementById("mainContainer")
  );
})();
