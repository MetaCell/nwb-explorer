import React from 'react';
import Icon from '@mui/material/Icon';


const style = {
  standard: {
    border: 0,
    background: 'transparent',
    padding: '0',
    width: '20px',
    height: '20px',
    boxShadow: 'none',
    minWidth: '10px',
    fontSize: '10px',
    hr: {},
  },
  lighter: { background: "var(primary-color)" },
  padding: {
    fontSize: 15,
    paddingTop: 1,
    paddingBottom: 1,
  },
};

const topLevelMenuItemStyle = {
  standard: { background: 'transparent' },
  hover: {},
};

const firstItemCustom = { fontWeight: 'bold' };

const firstItemStyle = {
  standard: { ...topLevelMenuItemStyle.standard, ...firstItemCustom },
  hover: { ...topLevelMenuItemStyle.hover, ...firstItemCustom },
};

const hiddenMenuItemStyle = {
  standard: { display: 'none' },
  hover: {},
};

export const listMenuConfigurations = (Instances, entity, availablePlots) => {
  const color = entity.color || '';
  const isImage = entity.type === 'ImageSeries';
  const arePlotsAvailable = availablePlots.length > 0;

  const config = {
    global: {
      color: '#ffffff',
      subMenuOpenOnHover: true,
      menuOpenOnClick: true,
      menuPadding: 0,
      fontFamily: "var(--font)",
      menuFontSize: '14',
      subMenuFontSize: '12',
      background: "var(--bg-regular)",
      buttonsStyle: {
        standard: style.standard,
        position: 'relative',
        hover: {
          ...style.standard,
          ...style.lighter,
        },
      },
      labelsStyle: {
        standard: { ...style.padding },
        hover: {
          ...style.lighter,
          ...style.padding,
        },
      },
      drawersStyle: {
        standard: {
          top: 10,
          backgroundColor: "var(--bg-dark)",
          borderRadius: 0,
          color: '#ffffff',
          fontSize: 14,
          fontFamily: "var(--font)",
          minWidth: 110,
          borderLeft: 0,
          borderRight: 0,
          borderBottom: 0,
          borderBottomLeftRadius: "var(--radius)",
          borderBottomRightRadius: "var(--radius)",
        },
      },
    },
    itemOptions: { customArrow: <i className="fa fa-caret-right menu-caret" /> },
    buttons: [
      {
        label: '',
        position: 'bottom-start',
        icon: <Icon className="fa fa-chevron-down" fontSize="small" />,
        list: [
          {
            label: 'Open in new plot',
            icon: '',
            action: { handlerAction: 'plot' },
            style: isImage ? hiddenMenuItemStyle : {},
          },
          {
            label: 'Add to an existing plot',
            icon: '',
            position: 'right',
            style: isImage || (!isImage && !arePlotsAvailable) ? hiddenMenuItemStyle : topLevelMenuItemStyle,
            dynamicListInjector: {
              handlerAction: 'menuInjector',
              parameters: ['AddPlot'],
            },
          },
          {
            label: <span>
              Colors
              <span>{color}</span>
            </span>,
            icon: '',
            position: 'right',
            style: isImage ? hiddenMenuItemStyle : topLevelMenuItemStyle,
            dynamicListInjector: {
              handlerAction: 'menuInjector',
              parameters: ['Color'],
            },
          },
          {
            label: 'Show Image Series',
            icon: '',
            action: { handlerAction: 'image' },
            style: !isImage ? hiddenMenuItemStyle : {},
          },
          {
            label: 'Show Details',
            icon: '',
            action: { handlerAction: 'details' },
          },
        ],
        style: firstItemStyle,
      },
    ],
  };
  return config;
};
