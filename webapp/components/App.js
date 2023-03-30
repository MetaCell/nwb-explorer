import React from 'react';
import WelcomePage from './pages/WelcomePage';
import nwbFileService from '../services/NWBFileService';
import FileExplorerPage from './pages/FileExplorerPage';

// import { Route, Switch, Redirect, BrowserRouter as Router } from 'react-router-dom';

export default class App extends React.Component {
  constructor () {
    super();
  }

  componentDidMount () {
    const { loadNWBFile, reset, model, nwbFileLoaded, raiseError, } = this.props;
    self = this;
    if (window !== window.parent) {
      window.parent.postMessage({ type: 'APP_READY' }, '*');
    }

    GEPPETTO.on(GEPPETTO.Events.Error_while_exec_python_command, error => {
      if (error) {
        raiseError(error);
      }
    });

    if (nwbFileService.getNWBFileUrl()) {
      loadNWBFile(nwbFileService.getNWBFileUrl());
    }

    const loadFromEvent = event => {
      // console.debug('Parent frame message received:', event)

      // Here we would expect some cross-origin check, but we don't do anything more than load a nwb file here
      switch (event.data.type) {
      case 'LOAD_RESOURCE':
        if (self.props.model) {
          reset();
        }
        loadNWBFile(event.data.payload);
        break;
      case 'NO_RESOURCE': {
        this.setState({ waitFile: false });
      }
      }
    };
    // A message from the parent frame can specify the file to load
    window.addEventListener('message', loadFromEvent);

    window.load = loadFromEvent;

    GEPPETTO.on(GEPPETTO.Events.Model_loaded, () => {
      nwbFileLoaded(Model);
    });


  }

  componentDidUpdate () {
    const {
      notebookReady, model, loading,
      isLoadedInNotebook, isLoadingInNotebook, error,
    } = this.props;

    if (!isLoadedInNotebook && model && notebookReady && !isLoadingInNotebook && !error) {
      // We may have missed the loading if notebook was not initialized at the time of the url change
    }

   
  }


  render () {
    const { nwbFileUrl } = this.props;

    let page;
    if (nwbFileUrl) {
      page = <FileExplorerPage />;
    } else {
      page = <WelcomePage />;
    }
    return (
      <div style={{ height: '100%', width: '100%' }}>
        <div id="main-container-inner">
          {page}
        </div>
        <div style={{ display: 'none' }}>
          {

            // getConsole()

          }
        </div>

      </div>
    );
  }
}
