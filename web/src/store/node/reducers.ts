import {
  GET_BRANCH_POINTS,
  GET_CURRENT_YEARLY_WIN,
  GET_CURRENT_YEARLY_PICK,
  NodeActionType,
  NodeState,
  GET_CURRENT_MOVES,
} from "./types";
import { INode } from "../../types";

const initState: NodeState = {
  branchPoints: { black: [], white: [] },
  currentMoves: new Set(),
  currentYearlyWin: [],
  currentYearlyPick: [],
};

export const nodeReducer = (
  state = initState,
  action: NodeActionType
): NodeState => {
  switch (action.type) {
    case GET_BRANCH_POINTS:
      var rawNodes: Array<INode> = action.payload;
      const blackMoves = rawNodes
        .filter((node) => node.color === "B")
        .map((node) => {
          return {
            id: node._id,
            x: node.move[0].charCodeAt(0) - 97,
            y: node.move[1].charCodeAt(0) - 97,
            color: node.color as "B" | "W",
          };
        });

      const whiteMoves = rawNodes
        .filter((node) => node.color === "W")
        .map((node) => {
          return {
            id: node._id,
            x: node.move[0].charCodeAt(0) - 97,
            y: node.move[1].charCodeAt(0) - 97,
            color: node.color as "B" | "W",
          };
        });

      return {
        ...state,
        branchPoints: { black: blackMoves, white: whiteMoves },
      };

    case GET_CURRENT_MOVES:
      return {
        ...state,
        currentMoves: action.payload,
      };

    case GET_CURRENT_YEARLY_WIN:
      return {
        ...state,
        currentYearlyWin: action.payload,
      };

    case GET_CURRENT_YEARLY_PICK:
      return {
        ...state,
        currentYearlyPick: action.payload,
      };

    default:
      return state;
  }
};
