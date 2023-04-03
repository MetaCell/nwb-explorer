import React, { lazy, Suspense } from 'react';
import NWBPlot from '../reduxconnect/NWBPlotContainer';
import CircularProgress from '@material-ui/core/CircularProgress';
import FileExplorerPage from '../pages/FileExplorerPage';
import Metadata from '../Metadata';
import NWBListViewer from '../reduxconnect/NWBListViewerContainer';
import SweepTableViewer from '../reduxconnect/SweepTableViewerContainer';
import ImageViewer from '../ImageViewer';
// import PythonConsole from '@metacell/geppetto-meta-ui/python-console/PythonConsole';


export class PythonConsole extends React.Component {
  constructor(props) {
    super(props);
  }

  shouldComponentUpdate(nextProps) {
    return nextProps.extensionLoaded !== this.props.extensionLoaded;
  }

  render() {

    return (
      <div className="col-lg-6 panel-body" id="pythonConsoleOutput">
        <iframe id="pythonConsoleFrame" src={this.props["pythonNotebookPath"]} marginWidth="0"
          marginHeight="0" frameBorder="no" scrolling="yes"
          allowtransparency="true"
          style={{
            width: '100%',
            visibility: !this.props.extensionLoaded ? "hidden" : "visible",
            height: this.props.iframeHeight + 'px'
          }}>
        </iframe>
        {!this.props.extensionLoaded && <CircularProgress
          style={{ position: 'absolute', left: 0, right: 0, bottom: 0, top: 0, margin: 'auto' }}
        />}
      </div>
    );
  }

}

console.log("init...");

export default {
  Explorer: FileExplorerPage,
  Metadata,
  ImageSeries: ImageViewer,
  Plot: NWBPlot,
  ListViewer: NWBListViewer,
  SweepTable: SweepTableViewer,
  PythonConsole: PythonConsole,
  placeholder: () => <div>Waiting data...</div>
};
