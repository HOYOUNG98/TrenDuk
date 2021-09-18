// library imports
import _ from "lodash";
import { IYearlyNode } from "../../types";

// local imports
import { NodeActionType, NodeState, GET_CURRENT_MOVES } from "./types";

const initState: NodeState = {
  currentMoves: [],
};

export const nodeReducer = (
  state = initState,
  action: NodeActionType
): NodeState => {
  var currentMoves: Array<IYearlyNode> = [];
  switch (action.type) {
    case GET_CURRENT_MOVES:
      currentMoves = action.payload;
      return {
        ...state,
        currentMoves,
      };

    default:
      return state;
  }
};
