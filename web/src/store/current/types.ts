import { INode } from "../../types";

export interface CurrentState {
  selectedNodes: Array<INode>;
  selectedColor: "B" | "W";
  hoverPoint: string;
}

export const SELECT_NODE = "SELECT_NODE";
export const SELECT_COLOR = "SELECT_COLOR";
export const UPDATE_HOVER_POINT = "UPDATE_HOVER_POINT";

interface selectNodeAction {
  type: typeof SELECT_NODE;
  payload: INode;
}

interface selectColorAction {
  type: typeof SELECT_COLOR;
}

interface updateHoverPoint {
  type: typeof UPDATE_HOVER_POINT;
  payload: string;
}

export type CurrentActionType =
  | selectNodeAction
  | selectColorAction
  | updateHoverPoint;
