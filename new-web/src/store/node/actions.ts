import { INode } from "../../types";
import { GET_BRANCH_POINTS, GET_BRANCH_STATS } from "./types";

export const getBranchPoints = (nodes: Array<INode>) => ({
  type: GET_BRANCH_POINTS,
  payload: nodes,
});

export const getWhiteBranchNodes = (nodes: Array<INode>) => ({
  type: GET_BRANCH_STATS,
  payload: nodes,
});
