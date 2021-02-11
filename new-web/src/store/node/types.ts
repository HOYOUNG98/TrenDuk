import { INode } from "../../types";

export interface NodeState {
  branchPoints: { black: Array<Object>; white: Array<Object> };
  branchStats: { black: Array<Object>; white: Array<Object> };
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
