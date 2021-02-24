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
  branchStats: { black: Array<INodeStats>; white: Array<INodeStats> };
}

export const GET_BRANCH_POINTS = "GET_BRANCH_POINTS";
export const GET_BRANCH_STATS = "GET_BRANCH_STATS";

interface getBranchPoints {
  type: typeof GET_BRANCH_POINTS;
  payload: Array<INode>;
}

interface getBranchStats {
  type: typeof GET_BRANCH_STATS;
  payload: Array<INode>;
}

export type NodeActionType = getBranchPoints | getBranchStats;
