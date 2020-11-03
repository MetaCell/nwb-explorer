import React from "react";
import {
  bgRegular,
  bgDark,
  font,
  primaryColor,
  gutter,
  radius,
} from "../../theme";

import { openDialog } from "../../redux/actions/general";

import { APPBAR_CONSTANTS, NWB_WEBSITE } from "../../constants";

const style = {
  standard: {
    background: bgRegular,
    borderRadius: 0,
    border: 0,
    boxShadow: "0px 0px",
    color: "#ffffff",
    paddingLeft: `calc(${gutter} * 2)`,
    paddingRight: `calc(${gutter} * 2)`,
    fontSize: 16,
    fontWeight: 400,
    fontFamily: font,
    margin: "0px 0px 0px 0px",
    height: "100%",
    borderLeft: 0,
    borderRight: 0,
    borderBottom: 0,
    textTransform: "capitalize",
    textAlign: "left",
    justifyContent: "start",

    hr: {},
  },
  lighter: { background: primaryColor },
  padding: {
    fontSize: 16,
    paddingTop: `calc(${gutter} / 2)`,
    paddingBottom: `calc(${gutter} / 2)`,
  },
};

const topLevelMenuItemStyle = {
  standard: { background: "transparent" },
  hover: {},
};

const firstItemCustom = {
  fontWeight: "bold",
  paddingLeft: `calc(${gutter} / 2)`,
};

const firstItemStyle = {
  standard: { ...topLevelMenuItemStyle.standard, ...firstItemCustom },
  hover: { ...topLevelMenuItemStyle.hover, ...firstItemCustom },
};

export default {
  global: {
    color: "white",
    subMenuOpenOnHover: true,
    menuOpenOnClick: true,
    menuPadding: 0,
    fontFamily: font,
    menuFontSize: "14",
    subMenuFontSize: "12",
    background: bgRegular,
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
        backgroundColor: bgDark,
        borderRadius: 0,
        color: "#ffffff",
        fontSize: 14,
        fontFamily: font,
        minWidth: 110,
        borderLeft: 0,
        borderRight: 0,
        borderBottom: 0,
        borderBottomLeftRadius: radius,
        borderBottomRightRadius: radius,
      },
    },
  },
  itemOptions: { customArrow: <i className="fa fa-caret-right menu-caret" /> },
  buttons: [
    {
      label: "NWB Explorer",
      position: "bottom-start",
      icon: "",
      list: [
        {
          label: APPBAR_CONSTANTS.HOME,
          icon: "",
          action: { handlerAction: APPBAR_CONSTANTS.HOME, },
        },
        {
          label: APPBAR_CONSTANTS.ABOUT,
          icon: "",
          action: {
            handlerAction: "redux",
            parameters: [
              openDialog,
              { title: APPBAR_CONSTANTS.ABOUT, message: "This is about tab" },
            ],
          },
        },
      ],
      style: firstItemStyle,
    },
    {
      label: "View",
      position: "bottom-start",
      icon: "",
      style: topLevelMenuItemStyle,
      list: [
        {
          label: APPBAR_CONSTANTS.SHOW_ALL_CONTENT,
          icon: "",
          action: { handlerAction: APPBAR_CONSTANTS.SHOW_ALL_CONTENT },
        },
        {
          label: APPBAR_CONSTANTS.RESTORE_VIEW,
          icon: "",
          action: { handlerAction: APPBAR_CONSTANTS.RESTORE_VIEW },
        },
      ],
    },
    {
      label: "Help",
      icon: "",
      position: "bottom-start",
      style: topLevelMenuItemStyle,
      list: [
        {
          label: APPBAR_CONSTANTS.DOCUMENTATION,
          icon: "",
          action: {
            handlerAction: APPBAR_CONSTANTS.NEW_PAGE,
            parameters: [NWB_WEBSITE],
          },
        },
      ],
    },
  ],
};

