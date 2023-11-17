import React from 'react';
import listViewerTableConf from './listViewerConfiguration';

const customConf = {
  id: 'sweep',
  title: 'Sweep',
  source: ({ path }) => Instances.getInstance(`${path}.sweep_number`).getValue().wrappedObj.value.text,
};
const conf = [...listViewerTableConf];
conf.splice(1, 0, customConf);
export default conf;
