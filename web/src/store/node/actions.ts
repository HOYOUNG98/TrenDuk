import { INode, IYearlyReChartData } from "../../types";
import {
  GET_BRANCH_POINTS,
  GET_CURRENT_YEARLY_WIN,
  GET_CURRENT_YEARLY_PICK,
  GET_CURRENT_MOVES,
} from "./types";

export const getBranchPoints = (nodes: Array<INode>) => ({
  type: GET_BRANCH_POINTS,
  payload: nodes,
});

export const getCurrentMoves = (moves: Array<INode>) => ({
  type: GET_CURRENT_MOVES,
  payload: moves,
});

export const getCurrentYearlyWin = (nodes: Array<IYearlyReChartData>) => ({
  type: GET_CURRENT_YEARLY_WIN,
  payload: nodes,
});

export const getCurrentYearlyPick = (nodes: Array<IYearlyReChartData>) => ({
  type: GET_CURRENT_YEARLY_PICK,
  payload: nodes,
});
