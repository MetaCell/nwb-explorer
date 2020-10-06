import React from "react";
import {
  bgRegular,
  bgDark,
  font,
  primaryColor,
  gutter,
  radius,
} from "../../theme";

const style = {
  standard: {
    border: 0,
    background: "transparent",
    padding: "0",
    width: "20px",
    height: "20px",
    boxShadow: "none",
    minWidth: "10px",
    fontSize: "10px",
    hr: {},
  },
  lighter: { background: primaryColor },
  padding: {
    fontSize: 15,
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
      position: "relative",
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
      label: "",
      position: "bottom-start",
      icon: "fa fa-chevron-down",
      list: [
        {
          label: "Open in new plot",
          icon: "",
          action: { handlerAction: "plot" },
        },
        {
          label: "Add to an existing plot",
          icon: "",
          position: "bottom-start",
          style: topLevelMenuItemStyle,
          dynamicListInjector: {
            handlerAction: "menuInjector",
            parameters: ["View"],
          },
        },
        {
          label: "Colors",
          icon: "",
          action: { handlerAction: "color" }
        },
        {
          label: "Show Details",
          icon: "",
          action: { handlerAction: "details" },
        },
      ],
      style: firstItemStyle,
    },
  ],
};

