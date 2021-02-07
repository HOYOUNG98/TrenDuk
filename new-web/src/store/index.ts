// library imports
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunkMiddleware from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";

import { nodeReducer } from "./node/reducers";
import { giboReducer } from "./gibo/reducers";
import { currentReducer } from "./current/reducers";

const middlewares = [thunkMiddleware];
const middlewareEnhancer = applyMiddleware(...middlewares);

const rootReducer = combineReducers({
  node: nodeReducer,
  gibo: giboReducer,
  current: currentReducer,
});

export const store = createStore(
  rootReducer,
  composeWithDevTools(middlewareEnhancer)
);

export type RootState = ReturnType<typeof rootReducer>;
