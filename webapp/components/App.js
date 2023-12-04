import React from 'react';
import WelcomePage from './pages/WelcomePage';
import nwbFileService from '../services/NWBFileService';
import FileExplorerPage from './pages/FileExplorerPage';

// import { Route, Switch, Redirect, BrowserRouter as Router } from 'react-router-dom';

export default class App extends React.Component {
  constructor () {
    super();
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
      </div>
    );
  }
}
