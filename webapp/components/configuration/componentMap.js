import React, { lazy, Suspense } from 'react';
import NWBPlot from '../reduxconnect/NWBPlotContainer';
import CircularProgress from '@material-ui/core/CircularProgress';
import FileExplorerPage from '../pages/FileExplorerPage';
import Metadata from '../Metadata';
import NWBListViewer from '../reduxconnect/NWBListViewerContainer';
import SweepTableViewer from '../reduxconnect/SweepTableViewerContainer';
import ImageViewer from '../ImageViewer';
// import PythonConsole from '@metacell/geppetto-meta-ui/python-console/PythonConsole';
import { PythonConsole } from '../reduxconnect';
import { getConsole } from '../../services/NotebookService';


console.log("init...");

export default {
  Explorer: FileExplorerPage,
  Metadata,
  ImageSeries: ImageViewer,
  Plot: NWBPlot,
  ListViewer: NWBListViewer,
  SweepTable: SweepTableViewer,
  PythonConsole: getConsole({ forceNew: GEPPETTO_CONFIGURATION.forceNewNotebook, useFilename: GEPPETTO_CONFIGURATION.oneFileOneNotebook }),
  placeholder: () => <div>Waiting data...</div>
};
