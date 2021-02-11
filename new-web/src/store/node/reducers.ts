import {
  GET_BRANCH_POINTS,
  GET_BRANCH_STATS,
  NodeActionType,
  NodeState,
} from "./types";
import { INode } from "../../types";

const initState: NodeState = {
  branchPoints: { black: [], white: [] },
  branchStats: { black: [], white: [] },
};

export const nodeReducer = (
  state = initState,
  action: NodeActionType
): NodeState => {
  switch (action.type) {
    case GET_BRANCH_POINTS:
      var rawNodes: Array<INode> = action.payload;
      const black = rawNodes
        .filter((node) => node.color === "B")
        .map((node) => {
          return {
            id: node._id,
            x: node.move[0].charCodeAt(0) - 97,
            y: node.move[1].charCodeAt(0) - 97,
            color: node.color,
          };
        });

      const white = rawNodes
        .filter((node) => node.color === "W")
        .map((node) => {
          return {
            id: node._id,
            x: node.move[0].charCodeAt(0) - 97,
            y: node.move[1].charCodeAt(0) - 97,
            color: node.color,
          };
        });
      return { ...state, branchPoints: { black, white } };

    case GET_BRANCH_STATS:
      return { ...state };

    default:
      return state;
  }
};
