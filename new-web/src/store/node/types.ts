import { INode } from "../../types";

export interface NodeState {
  blackBranchNodes: Array<INode>;
  whiteBranchNodes: Array<INode>;
}

export const GET_BLACK_BRANCH_NODES = "GET_BLACK_BRANCH_NODES";
export const GET_WHITE_BRANCH_NODES = "GET_WHITE_BRANCH_NODES";

interface getBlackBranchNodesAction {
  type: typeof GET_BLACK_BRANCH_NODES;
  payload: Array<INode>;
}

interface getWhiteBranchNodesAction {
  type: typeof GET_WHITE_BRANCH_NODES;
  payload: Array<INode>;
}

export type NodeActionType =
  | getBlackBranchNodesAction
  | getWhiteBranchNodesAction;
