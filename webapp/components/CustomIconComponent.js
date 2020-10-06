import React from 'react';
import Button from "@material-ui/core/IconButton";
import RemoveRedEyeIcon from "@material-ui/icons/RemoveRedEye";

const IconComponent = ({ action, color, tooltip }) => (
  <Button
    style={{ color }}
    className="list-icon"
    title={tooltip}
    onClick={action}
  >
    <RemoveRedEyeIcon />
  </Button>
)

export const CustomIconComponent = ({ icon, action, color, tooltip, defaultColor }) => ({ value, }) => (
  <IconComponent
    color={color}
    defaultColor={defaultColor}
    title={tooltip}
    action={() => action(value)}
    icon={icon}
  />
);
