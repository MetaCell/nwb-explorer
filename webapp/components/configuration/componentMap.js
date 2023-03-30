import React, { lazy, Suspense } from 'react';
import NWBPlot from '../reduxconnect/NWBPlotContainer';
import FileExplorerPage from '../pages/FileExplorerPage';
import Metadata from '../Metadata';
import NWBListViewer from '../reduxconnect/NWBListViewerContainer';
import SweepTableViewer from '../reduxconnect/SweepTableViewerContainer';
import ImageViewer from '../ImageViewer';
import { getConsole } from '../../services/NotebookService';

export default {
  Explorer: FileExplorerPage,
  Metadata,
  ImageSeries: ImageViewer,
  Plot: NWBPlot,
  ListViewer: NWBListViewer,
  SweepTable: SweepTableViewer,
  PythonConsole: () => getConsole(GEPPETTO_CONFIGURATION.forceNewNotebook, GEPPETTO_CONFIGURATION.oneFileOneNotebook),
  placeholder: () => <div>Waiting data...</div>
};
