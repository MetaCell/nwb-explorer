import React, { Fragment } from 'react';

import { layoutManager } from '../../redux/store';
import Appbar from '../reduxconnect/AppBarContainer';
import Dialog from '../reduxconnect/DialogContainer';
import layout from '../configuration/layout';
import { Box } from '@mui/material';

export default () => {
  const LayoutComponent = layoutManager?.getComponent();
  return (
    <Box height="100%" width="100%" display="flex" flexDirection="column">
      <Appbar />
      {LayoutComponent && <LayoutComponent layout={layout} /> }
      <Dialog />
    </Box>
  );
};
