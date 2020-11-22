import { INode } from "../../types";

export interface StateState {
  selectedNode: INode | null;
  selectedNodes: Array<INode>;
  selectedColor: "B" | "W";
}

export const SELECT_NODE = "SELECT_NODE";
export const SELECT_COLOR = "SELECT_COLOR";

interface selectNodeAction {
  type: typeof SELECT_NODE;
  payload: INode;
}

interface selectColorAction {
  type: typeof SELECT_COLOR;
}

export type StateActionType = selectNodeAction | selectColorAction;
