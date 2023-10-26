import React, { Component } from 'react';
import { GroupComponent } from '@metacell/geppetto-meta-ui/list-viewer/ListViewer';
import RemoveRedEyeIcon from '@material-ui/icons/RemoveRedEye';
import { FILEVARIABLE_LENGTH } from '../../constants';
import { CustomIconComponent } from '../CustomIconComponent';
import ListControlsComponent from '../ListMenuComponent';

const iconUnselectedColor = 'rgba(255, 255, 255, 0.3)';
const conf = [
  {
    id: 'controls',
    title: 'Controls',
    customComponent: GroupComponent,

    configuration: [
      {
        id: 'showPlot',
        customComponent: CustomIconComponent,
        visible: entity => entity.type !== 'ImageSeries'
          && Instances.getInstance(`${entity.path}.data`)
          && Instances.getInstance(`${entity.path}.timestamps`),

        source: entity => entity,
        configuration: {
          action: 'clickShowPlot',
          label: 'Plot',
          tooltip: 'Plot time series',
          color: iconUnselectedColor,
          icon: RemoveRedEyeIcon,
          defaultColor: entity => entity.color,
        },
      },
      {
        id: 'image',
        customComponent: CustomIconComponent,
        visible: entity => entity.type === 'ImageSeries',
        source: entity => entity,
        configuration: {
          action: 'clickShowImg',
          icon: RemoveRedEyeIcon,
          label: 'Plot',
          tooltip: 'Plot image series',
          color: iconUnselectedColor,
          defaultColor: entity => entity.color,
        },
      },
      {
        id: 'showDetails',
        customComponent: CustomIconComponent,
        visible: entity => !((Instances.getInstance(`${entity.path}.data`)
            && Instances.getInstance(`${entity.path}.timestamps`)) || entity.type === 'ImageSeries'),
        source: entity => entity,
        configuration: {
          action: 'clickShowDetails',
          label: 'Show details',
          tooltip: 'Show details',
          color: iconUnselectedColor,
          icon: RemoveRedEyeIcon,
          defaultColor: entity => entity.color,
        },
      },
      {
        id: 'menuOptions',
        customComponent: ListControlsComponent,
        source: entity => entity,
        visible: entity => (Instances.getInstance(`${entity.path}.data`)
            && Instances.getInstance(`${entity.path}.timestamps`)) || entity.type === 'ImageSeries',
        configuration: {
          actions: 'clickShowDetails',
          label: 'Show details',
          tooltip: 'Show details',
          color: '#ffffff',
        },
      },
    ],
  },
  {
    id: 'path',
    title: 'Path',
    customComponent: ({ action }) => ({ value }) => <span onClick={() => action(value)} style={{ cursor: 'pointer' }}>{value}</span>,
    source: ({ path }) => path.slice(FILEVARIABLE_LENGTH),
    configuration: { action: 'clickTitleDetails' },

  },
  {
    id: 'type',
    title: 'Type',
    source: 'type',
  },
  {
    id: 'description',
    title: 'Description',
    source: 'description',
  },
];

export default conf;
