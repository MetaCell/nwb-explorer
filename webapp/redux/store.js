import { createStore, applyMiddleware, compose } from "redux";
import all from "./reducers/all";
import { GENERAL_DEFAULT_STATUS } from "./reducers/general";
import { NOTEBOOK_DEFAULT_STATUS } from "./reducers/notebook";
import { NWBFILE_DEFAULT_STATUS } from "./reducers/nwbfile";
import { FLEXLAYOUT_DEFAULT_STATUS } from "./reducers/flexlayout";
import nwbMiddleware from './middleware/nwbMiddleware';

const INIT_STATE = { 
  general: GENERAL_DEFAULT_STATUS,
  nwbfile: NWBFILE_DEFAULT_STATUS,
  notebook: NOTEBOOK_DEFAULT_STATUS,
  flexlayout: FLEXLAYOUT_DEFAULT_STATUS
};

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;


function configureStore (state = INIT_STATE) {
  return createStore(
    all,
    state,
    composeEnhancers(applyMiddleware(nwbMiddleware))
  );
}

export default configureStore;