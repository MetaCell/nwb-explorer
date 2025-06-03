import React from 'react';


import { openDialog } from '../../redux/actions/general';

import { APPBAR_CONSTANTS, NWBE_WEBSITE, NWB_WEBSITE } from '../../constants';

const style = {
  standard: {
    background: "var(--bg-regular)",
    borderRadius: 0,
    border: 0,
    boxShadow: '0px 0px',
    color: '#ffffff',
    paddingLeft: `calc(var(--gutter) * 2)`,
    paddingRight: `calc(var(--gutter) * 2)`,
    fontSize: 16,
    fontWeight: 400,
    fontFamily: "var(--font)",
    margin: '0px 0px 0px 0px',
    height: '100%',
    borderLeft: 0,
    borderRight: 0,
    borderBottom: 0,
    textTransform: 'capitalize',
    textAlign: 'left',
    justifyContent: 'start',

    hr: {},
  },
  lighter: { background: "var(--primary-color)" },
  padding: {
    fontSize: 16,
    paddingTop: `calc(var(--gutter) / 2)`,
    paddingBottom: `calc(var(--gutter) / 2)`,
  },
};

const topLevelMenuItemStyle = {
  standard: { background: 'transparent' },
  hover: {},
};

const firstItemCustom = {
  fontWeight: 'bold',
  paddingLeft: 1,
};

const firstItemStyle = {
  standard: { ...topLevelMenuItemStyle.standard, ...firstItemCustom },
  hover: { ...topLevelMenuItemStyle.hover, ...firstItemCustom },
};

export default {
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
      label: 'NWB Explorer',
      position: 'bottom-start',
      icon: '',
      list: [
        {
          label: APPBAR_CONSTANTS.HOME,
          icon: '',
          action: { handlerAction: APPBAR_CONSTANTS.HOME },
        },
        {
          label: APPBAR_CONSTANTS.ABOUT,
          icon: '',
          action: {
            handlerAction: 'redux',
            parameters: [
              openDialog,
              { title: APPBAR_CONSTANTS.ABOUT, message: 'This is about tab' },
            ],
          },
        },
      ],
      style: firstItemStyle,
    },
    {
      label: 'View',
      position: 'bottom-start',
      icon: '',
      style: topLevelMenuItemStyle,
      list: [
        {
          label: APPBAR_CONSTANTS.SHOW_ALL_CONTENT,
          icon: '',
          action: { handlerAction: APPBAR_CONSTANTS.SHOW_ALL_CONTENT },
        },
        {
          label: APPBAR_CONSTANTS.RESTORE_VIEW,
          icon: '',
          action: { handlerAction: APPBAR_CONSTANTS.RESTORE_VIEW },
        },
      ],
    },
    {
      label: 'Help',
      icon: '',
      position: 'bottom-start',
      style: topLevelMenuItemStyle,
      list: [
        {
          label: APPBAR_CONSTANTS.NWBE_DOCUMENTATION,
          icon: '',
          action: {
            handlerAction: APPBAR_CONSTANTS.NEW_PAGE,
            parameters: [NWBE_WEBSITE],
          },
        },
        {
          label: APPBAR_CONSTANTS.NWB_DOCUMENTATION,
          icon: '',
          action: {
            handlerAction: APPBAR_CONSTANTS.NEW_PAGE,
            parameters: [NWB_WEBSITE],
          },
        },
      ],
    },
  ],
};
