import { IYearlyNode } from "../../types";

export interface INodeMoves {
  id: string;
  x: number;
  y: number;
  color: "B" | "W";
}

export interface NodeState {
  currentMoves: Array<IYearlyNode>;
}

export const GET_CURRENT_MOVES = "GET_CURRENT_MOVES";

interface getCurrentMoves {
  type: typeof GET_CURRENT_MOVES;
  payload: Array<IYearlyNode>;
}

export type NodeActionType = getCurrentMoves;
