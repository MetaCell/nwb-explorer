import React, { Fragment } from 'react';

import { getLayoutManagerInstance } from '@metacell/geppetto-meta-client/common/layout/LayoutManager';
import Appbar from '../reduxconnect/AppBarContainer';
import Dialog from '../reduxconnect/DialogContainer';
import layout from '../configuration/layout';
import { Box } from '@mui/material';

export default () => {
  const LayoutComponent = React.useState(null)
  React.useEffect(() => 
    setTimeout(() => getLayoutManagerInstance().getComponent(), 500)
  , [])
  return (
    <Box height="100%" width="100%" display="flex" flexDirection="column">
      <Appbar />
      {LayoutComponent && <LayoutComponent layout={layout} /> }
      <Dialog />
    </Box>
  );
};
