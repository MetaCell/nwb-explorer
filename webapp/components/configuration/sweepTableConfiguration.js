import React from 'react';

const conf = [
  {
    id: "sweep",
    title: "Sweep #",
    source: ({ path }) => Instances.getInstance(path + '.sweep_number').getValue().wrappedObj.value.text,
  }
  
];

export default conf;