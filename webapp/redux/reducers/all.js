import { combineReducers } from 'redux';

import general from './general';
import nwbfile from './nwbfile';
import notebook from './notebook';
import flexlayout from './flexlayout';

export default combineReducers({
  general,
  nwbfile,
  notebook,
  flexlayout
});