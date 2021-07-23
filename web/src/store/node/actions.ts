import { INode } from "../../types";
import {
  GET_BRANCH_POINTS,
  GET_CURRENT_YEARLY_WIN,
  GET_CURRENT_YEARLY_PICK,
} from "./types";

export const getBranchPoints = (nodes: Array<INode>) => ({
  type: GET_BRANCH_POINTS,
  payload: nodes,
});

export const getCurrentYearlyWin = (nodes: Array<Object>) => ({
  type: GET_CURRENT_YEARLY_WIN,
  payload: nodes,
});

export const getCurrentYearlyPick = (nodes: Array<Object>) => ({
  type: GET_CURRENT_YEARLY_PICK,
  payload: nodes,
});
