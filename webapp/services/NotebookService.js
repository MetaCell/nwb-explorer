import PythonConsole from '@metacell/geppetto-meta-ui/python-console/PythonConsole';
import React from 'react';
import NWBFileService from './NWBFileService';

export function getNotebookPath (forceNew = true, useFilename = true) {
  if (GEPPETTO_CONFIGURATION.notebookName) {
    return `notebook?path=${GEPPETTO_CONFIGURATION.notebookName}`;
  }
  const nwbFileParam = NWBFileService.getNWBFileUrl();
  if (nwbFileParam && useFilename) {
    return `notebook?path=workspace/${nwbFileParam.split('/').slice(-1)}.ipynb`;
  }
  const key = forceNew ? Math.random().toString(36).slice(3) : '';

  return `notebook?path=workspace/nwbexplorer${key}.ipynb`;
}



let console = null;

// export function getConsole (forceNew = true, useFilename = true) {
//   if (console === null) {
//     console = [<PythonConsole pythonNotebookPath="notebooks/notebook.ipynb" extensionLoaded={this.props.extensionLoaded} /><iframe key="console" src={getNotebookPath(forceNew, useFilename)} />];
//   }
//   return console;
// }
