import React from 'react';
import SplashPage from './pages/SplashPage';
import nwbFileService from '../services/NWBFileService';
import FileExplorerPage from './pages/FileExplorerPage';
// import { Route, Switch, Redirect, BrowserRouter as Router } from 'react-router-dom';

export default class App extends React.Component{

  constructor (props, context) {
    super(props, context);
  }

  componentDidMount () {
    const { loadNWBFile, loadNotebook, notebookReady, nwbFileLoaded, raiseError } = this.props;
    self = this;

    
    GEPPETTO.on(GEPPETTO.Events.Error_while_exec_python_command, error => {
      if (error) {
        raiseError(error);
      }
    })

    if (nwbFileService.getNWBFileUrl()){
      loadNWBFile(nwbFileService.getNWBFileUrl());
    }

    // A message from the parent frame can specify the file to load
    window.addEventListener('message', event => {

      // Here we would expect some cross-origin check, but we don't do anything more than load a nwb file here
      if (typeof (event.data) == 'string') {
        loadNWBFile(event.data);
        // The message may be triggered after the notebook was ready

      }
    });
   
    
    GEPPETTO.on(GEPPETTO.Events.Model_loaded, () => {
      nwbFileLoaded(Model);
    });

    
    GEPPETTO.on(GEPPETTO.Events.Hide_spinner, () => {
      // Handles when Geppetto is hiding the spinner on its logic
      if (Object.values(this.props.loading).length !== 0) {
        this.showSpinner(this.props.loading);
      }
    });
       
  }

  componentDidUpdate () {
    const {
      notebookReady, model, loading, 
      isLoadedInNotebook, isLoadingInNotebook, error
    } = this.props;
    

    if (!isLoadedInNotebook && model && notebookReady && !isLoadingInNotebook && !error) {
      // We may have missed the loading if notebook was not initialized at the time of the url change
    }

    // It would be better having the spinner as a parametrized react component
    if (Object.values(loading).length !== 0) {
      this.showSpinner(loading);
    } else {
      GEPPETTO.trigger(GEPPETTO.Events.Hide_spinner);
    }
   
    
  }
 
 
  showSpinner (loading) {
    if (Object.values(loading).length !== 0) {
      const msg = Object.values(loading)[0];
      setTimeout(() => {
        GEPPETTO.trigger(GEPPETTO.Events.Show_spinner, msg);
      }, 500);
    } 
  }

  render () {
    const { model, embedded, showNotebook, isLoadedInNotebook, nwbFileUrl } = this.props;
    
    var page;
    if (nwbFileUrl) {
      page = <FileExplorerPage/>
    } else if (!embedded) {
      page = <SplashPage />
    } else {
      page = '<h1>Waiting for data...</h1>';
    }
    return (
      <div style={{ height: '100%', width: '100%' }}>
        <div id="main-container-inner">
          { page }
        </div>
        <div style={{ display: "none" }}>
          {

            // getConsole()

          }
        </div>
        
      </div>
    )
  }
}


