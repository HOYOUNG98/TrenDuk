import { INode } from "../../types";
import { SELECT_NODE, SELECT_COLOR, UPDATE_HOVER_POINT } from "./types";

export const selectNode = (node: INode) => ({
  type: SELECT_NODE,
  payload: node,
});

export const selectColor = () => ({
  type: SELECT_COLOR,
});

export const updateHoverPoint = (hoverPoint: string) => ({
  type: UPDATE_HOVER_POINT,
  payload: hoverPoint,
});
