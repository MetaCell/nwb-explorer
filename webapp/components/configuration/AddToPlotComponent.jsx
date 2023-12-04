import React from 'react';

import AddPlotMenuConnect from '../reduxconnect/AddPlotMenuConnect';

const AddToPlotComponent = ({ icon, label, action, tooltip }) => ({ value }) => (
  <AddPlotMenuConnect 
    icon={icon}  
    action={action} 
    instancePath={value.path}
  />
)

export default AddToPlotComponent;