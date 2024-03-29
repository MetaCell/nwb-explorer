import { PythonConsole } from '../components/reduxconnect';
import React, { useMemo } from 'react';
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


export const getConsole = ( forceNew = true, useFilename = true ) => () => <PythonConsole key="console" pythonNotebookPath={getNotebookPath(forceNew, useFilename)} />
