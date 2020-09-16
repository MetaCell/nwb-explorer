import React from 'react';
import { GroupComponent, IconComponent, ColorComponent } from "geppetto-client/js/components/interface/listViewer/ListViewer";


import AddToPlotComponent from './AddToPlotComponent';

import { FILEVARIABLE_LENGTH } from '../constants';
``
const conf = [
  {
    id: "path",
    title: "Path",
    source: ({ path }) => path.slice(FILEVARIABLE_LENGTH),
  },
  {
    id: "type",
    title: "Type",
    source: "type"
  },
  {
    id: "description",
    title: "Description",
    source: 'description',
  },
  
  {
    id: "controls",
    title: "Controls",
    customComponent: GroupComponent,
      
    configuration: [
      {
        id: "showdetails",
        customComponent: IconComponent,
        configuration: {
          action: "clickShowDetails",
          icon: "info-circle",
          label: "Show details",
          tooltip: "Show details",
        },
      },
      {
        id: "plot",
        customComponent: ColorComponent,
        visible: entity => Instances.getInstance(entity.path + '.data') && Instances.getInstance(entity.path + '.timestamps'),
        source: entity => entity,
        configuration: {
          action: "clickShowPlot",
          icon: "area-chart",
          label: "Plot",
          tooltip: "Plot time series",
          defaultColor: entity => Instances.getInstance(entity.path).color,
          
        },
      },
      {
        id: "image",
        customComponent: IconComponent,
        visible: entity => entity.type === 'ImageSeries',
        source: entity => entity,
        configuration: {
          action: "clickShowImg",
          icon: "picture-o",
          label: "Plot",
          tooltip: "Plot image series"
        },
      },
      {
        id: "addToPlot",
        customComponent: AddToPlotComponent,
        visible: entity => Instances.getInstance(entity.path + '.data') && Instances.getInstance(entity.path + '.timestamps'),
        configuration: {
          icon: "gpt-addplot",
          action: "clickAddToPlot",
          label: "Add Plot",
          tooltip: "Add plot",
        }
      }
    ]
  },
  
];

export default conf;