import { INode } from "../../types";
import { GET_WHITE_BRANCH_NODES, GET_BLACK_BRANCH_NODES } from "./types";

export const getBlackBranchNodes = (nodes: Array<INode>) => ({
  type: GET_BLACK_BRANCH_NODES,
  payload: nodes,
});

export const getWhiteBranchNodes = (nodes: Array<INode>) => ({
  type: GET_WHITE_BRANCH_NODES,
  payload: nodes,
});
