import { INode } from "../../types";

export interface INodeMoves {
  id: string;
  x: number;
  y: number;
  color: "B" | "W";
}

export interface IYearly {
  year: string;
  count: number;
  win?: number;
  lose?: number;
}

export interface INodeStats {
  color: string;
  id: string;
  yearlyStat: Array<IYearly>;
}

export interface NodeState {
  branchPoints: { black: Array<INodeMoves>; white: Array<INodeMoves> };
  currentYearlyWin: Array<Object>;
  currentYearlyPick: Array<Object>;
}

export const GET_BRANCH_POINTS = "GET_BRANCH_POINTS";
export const GET_CURRENT_YEARLY_WIN = "GET_CURRENT_YEARLY_WIN";
export const GET_CURRENT_YEARLY_PICK = "GET_CURRENT_YEARLY_PICK";

interface getBranchPoints {
  type: typeof GET_BRANCH_POINTS;
  payload: Array<INode>;
}

interface getCurrentYearlyWin {
  type: typeof GET_CURRENT_YEARLY_WIN;
  payload: Array<Object>;
}

interface getCurrentYearlyPick {
  type: typeof GET_CURRENT_YEARLY_PICK;
  payload: Array<Object>;
}

export type NodeActionType =
  | getBranchPoints
  | getCurrentYearlyWin
  | getCurrentYearlyPick;
