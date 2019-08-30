import NWBFileService from './NWBFileService';
import PythonConsole from 'geppetto-client/js/components/interface/pythonConsole/PythonConsole';
import React from 'react';

export function getNotebookPath () {
  const nwbFileParam = NWBFileService.getNWBFileUrl();
  if (nwbFileParam){
    return "notebook?path=" + nwbFileParam.split('/').slice(-1) + '.ipynb';
  }
  return "notebooks/notebook.ipynb";
}

var console = null;


export function getConsole () {
  if (console === null) {
    console = [<PythonConsole key="console" pythonNotebookPath={getNotebookPath()} />]
  }
  return console;
}
