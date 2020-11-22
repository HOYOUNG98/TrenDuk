import { INode } from "../../types";
import { SELECT_NODE, SELECT_COLOR } from "./types";

export const selectNode = (node: INode) => ({
  type: SELECT_NODE,
  payload: node,
});

export const selectColor = () => ({
  type: SELECT_COLOR,
});
