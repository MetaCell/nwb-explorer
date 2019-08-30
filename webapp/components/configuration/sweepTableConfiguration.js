import React from 'react';
import { GroupComponent, IconComponent, ColorComponent } from "geppetto-client/js/components/interface/listViewer/ListViewer";
import AddPlotMenuConnect from '../reduxconnect/AddPlotMenuConnect';

const AddToPlotComponent = ({ icon, label, action, tooltip }) => ({ value }) => (
  <AddPlotMenuConnect 
    icon={icon}  
    action={action} 
    instancePath={value.path}
  />
)

import { FILEVARIABLE_LENGTH } from '../constants';
``
const conf = [
  {
    id: "sweep",
    title: "Sweep #",
    source: ({ path }) => Instances.getInstance(path + '.sweep_number').getValue().wrappedObj.value.text,
  },
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
        source: entity => entity,
        configuration: {
          action: "clickShowPlot",
          icon: "area-chart",
          label: "Plot",
          tooltip: "Plot time series",
          defaultColor: entity => entity.color,
          
        },
      },
      {
        id: "addToPlot",
        customComponent: AddToPlotComponent,
        visible: true,
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