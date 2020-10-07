import React, { Fragment } from 'react';
import LayoutManager from '../reduxconnect/LayoutManagerContainer';
import Appbar from '../reduxconnect/AppBarContainer'
import Dialog from '../reduxconnect/DialogContainer'
import layout from '../configuration/layout.json';

export default model => (
  <Fragment>
    <Appbar/>
    <LayoutManager layout= {layout}/>
    <Dialog/>
  </Fragment>
)