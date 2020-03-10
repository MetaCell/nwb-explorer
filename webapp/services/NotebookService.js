import NWBFileService from './NWBFileService';
import PythonConsole from 'geppetto-client/js/components/interface/pythonConsole/PythonConsole';
import React from 'react';

export function getNotebookPath () {
  const nwbFileParam = NWBFileService.getNWBFileUrl();
  if (nwbFileParam){
    return "notebook?path=" + nwbFileParam.split('/').slice(-1) + '.ipynb';
  }
  const key = Math.random().toString(36).slice(3);

  return "notebook?path=nwbnotebook" + key + '.ipynb';
}

var console = null;


export function getConsole () {
  if (console === null) {
    console = [<PythonConsole key="console" pythonNotebookPath={getNotebookPath()} />]
  }
  return console;
}
