import React from 'react';
import Button from "@material-ui/core/IconButton";
import RemoveRedEyeIcon from "@material-ui/icons/RemoveRedEye";

const IconComponent = ({ Icon, action, color, tooltip }) =>
  <Button
    style={{ color: color }}
    className="list-icon"
    title={tooltip}
    onClick={action}
  >
    <RemoveRedEyeIcon />
  </Button>

export const CustomIconComponent = ({ icon, action, color, tooltip }) => ({ value, }) => (
  <IconComponent
    color={color}
    title={tooltip}
    action={() => action(value)}
    icon={icon}
  />
);
