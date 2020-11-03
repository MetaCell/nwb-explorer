import React, { Component } from 'react';
import ListViewer from '@geppettoengine/geppetto-ui/list-viewer/ListViewer';
import NWBListViewer from './NWBListViewer';
import listViewerTableConf from './configuration/listViewerConfiguration';
import sweepTableConf from './configuration/sweepTableConfiguration';

const DEFAULT_MODEL_SETTINGS = { color:  'white' };
const TYPE_INCLUDE_REGEX = /^(?!.*details)Model.nwbfile.*$/;


export default class SweepTableViewer extends NWBListViewer {

  constructor (props) {
    super(props);
  }

  filter (pathObj) {
    const { path, type } = pathObj;

    if (type.match(TYPE_INCLUDE_REGEX)) {
      const instance = Instances.getInstance(path);
      if (instance.getType) {
        const instanceType = instance.getType();
        return instanceType.sweep_number && !instanceType.series_index;
      }
    } 

    return false;
    
  }


  getColumnConfiguration () {
    return sweepTableConf.concat(listViewerTableConf);
  }
  
  
}

