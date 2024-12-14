import React from 'react';
import WelcomePage from './pages/WelcomePage';
import FileExplorerPage from './pages/FileExplorerPage';


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
