import Utils from '../Utils';

export const LOAD_NOTEBOOK = 'LOAD_NOTEBOOK';
export const UNLOAD_NOTEBOOK = 'UNLOAD_NOTEBOOK';
export const NOTEBOOK_READY = 'NOTEBOOK_READY';


export const loadNotebook = { type: LOAD_NOTEBOOK };

export const unloadNotebook = { type: UNLOAD_NOTEBOOK };

export const notebookReady = { type: NOTEBOOK_READY };
