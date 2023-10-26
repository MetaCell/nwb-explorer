import { combineReducers } from 'redux';

import general from './general';
import nwbfile from './nwbfile';
import notebook from './notebook';

export default {
  general,
  nwbfile,
  notebook,
};
