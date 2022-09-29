import React from "react";
import Icon from '@material-ui/core/Icon';

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

const firstItemCustom = { fontWeight: "bold" };

const firstItemStyle = {
  standard: { ...topLevelMenuItemStyle.standard, ...firstItemCustom },
  hover: { ...topLevelMenuItemStyle.hover, ...firstItemCustom },
};

const hiddenMenuItemStyle = {
  standard: { display: "none" },
  hover: {},
};

export const listMenuConfigurations = (Instances, entity, availablePlots) => {
  const color = entity.color || "";
  const isImage = entity.type === "ImageSeries";
  const arePlotsAvailable = availablePlots.length > 0

  const config = {
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
        icon: <Icon className='fa fa-chevron-down' fontSize="small" />,
        list: [
          {
            label: "Open in new plot",
            icon: "",
            action: { handlerAction: "plot" },
            style: isImage ? hiddenMenuItemStyle : {},
          },
          {
            label: "Add to an existing plot",
            icon: "",
            position: "right",
            style: isImage || (!isImage && !arePlotsAvailable) ? hiddenMenuItemStyle : topLevelMenuItemStyle,
            dynamicListInjector: {
              handlerAction: "menuInjector",
              parameters: ["AddPlot"],
            },
          },
          {
            label: <span>Colors <span>{color}</span></span>,
            icon: "",
            position: "right",
            style: isImage ? hiddenMenuItemStyle : topLevelMenuItemStyle,
            dynamicListInjector: {
              handlerAction: "menuInjector",
              parameters: ["Color"],
            },
          },
          {
            label: "Show Image Series",
            icon: "",
            action: { handlerAction: "image" },
            style: !isImage ? hiddenMenuItemStyle : {},
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
  return config;
};
