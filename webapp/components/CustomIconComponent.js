import React from 'react';
import IconButton from '@material-ui/core/IconButton';
import { isString } from '../Utils';

const IconComponent = ({ action, color, tooltip, Icon, }) => (
  <IconButton
    style={{ color }}
    className="list-icon"
    title={tooltip}
    onClick={action}
  >
    <Icon />
  </IconButton>
);

export const CustomIconComponent = ({ icon, action, color, tooltip, defaultColor, }) => ({ value }) => {
  if (defaultColor) {
    color = isString(defaultColor) ? defaultColor : defaultColor(value);
  }
  if (!color) {
    color = 'rgba(255, 255, 255, 0.3)';
  }
  return (
    <IconComponent
      color={color}
      defaultColor={defaultColor}
      title={tooltip}
      action={() => action(value)}
      Icon={icon}
    />
  );
};
