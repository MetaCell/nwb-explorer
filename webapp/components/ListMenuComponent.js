import React from 'react';
import ListMenuComponentConnect from './reduxconnect/ListMenuContainer';

const ListControlsComponent = ({ icon, actions, color, tooltip, }) => ({ value }) => (
  <ListMenuComponentConnect
    color={color}
    title={tooltip}
    actions={() => actions(value)}
    icon={icon}
    entity={value}
  />
);

export default ListControlsComponent;
