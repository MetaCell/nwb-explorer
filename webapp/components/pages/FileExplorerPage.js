import React, { Fragment } from 'react';

import { getLayoutManagerInstance } from '@metacell/geppetto-meta-client/common/layout/LayoutManager';
import Appbar from '../reduxconnect/AppBarContainer';
import Dialog from '../reduxconnect/DialogContainer';
import layout from '../configuration/layout';

export default () => {
  const LayoutManager = getLayoutManagerInstance().getComponent();
  return (
    <>
      <Appbar />
      <LayoutManager layout={layout} />
      <Dialog />
    </>
  );
};
