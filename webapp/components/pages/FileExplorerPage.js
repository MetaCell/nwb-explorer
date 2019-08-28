import React, { Fragment } from 'react';
import LayoutManager from '../reduxconnect/LayoutManagerContainer';
import Appbar from '../reduxconnect/AppBarContainer'
import layout from '../configuration/layout.json';
export default model => (
  <Fragment>
    <Appbar/>
    <LayoutManager layout= {layout}/>
  </Fragment>
)