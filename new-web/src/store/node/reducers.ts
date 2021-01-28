import {
  GET_BLACK_BRANCH_NODES,
  GET_WHITE_BRANCH_NODES,
  NodeActionType,
  NodeState,
} from "./types";
import { INode } from "../../types";

const initState: NodeState = {
  blackBranchNodes: [],
  whiteBranchNodes: [],
};

export const nodeReducer = (
  state = initState,
  action: NodeActionType
): NodeState => {
  let blackBranchNodes: Array<INode>;
  let whiteBranchNodes: Array<INode>;

  switch (action.type) {
    case GET_BLACK_BRANCH_NODES:
      blackBranchNodes = action.payload;
      return { ...state, blackBranchNodes };

    case GET_WHITE_BRANCH_NODES:
      whiteBranchNodes = action.payload;
      return { ...state, whiteBranchNodes };

    default:
      return state;
  }
};
