import { createStore } from '@metacell/geppetto-meta-client/common';
import all from './reducers/all';
import { GENERAL_DEFAULT_STATUS } from './reducers/general';
import { NOTEBOOK_DEFAULT_STATUS } from './reducers/notebook';
import { NWBFILE_DEFAULT_STATUS } from './reducers/nwbfile';

import nwbMiddleware from './middleware/nwbMiddleware';

import baseLayout from '../components/configuration/layout';
import componentMap from '../components/configuration/componentMap';

const INIT_STATE = {
  general: GENERAL_DEFAULT_STATUS,
  nwbfile: NWBFILE_DEFAULT_STATUS,
  notebook: NOTEBOOK_DEFAULT_STATUS,
  widgets: {}
};

function configureStore (state = INIT_STATE) {
  return createStore(
    all,
    state,
    [nwbMiddleware],
    { baseLayout, componentMap },
  );
}

export default configureStore;
