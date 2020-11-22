import {
  StateState,
  StateActionType,
  SELECT_NODE,
  SELECT_COLOR,
} from "./types";
import { INode } from "../../types";

const initState: StateState = {
  selectedNode: null,
  selectedNodes: [],
  selectedColor: "B",
};

export const stateReducer = (
  state = initState,
  action: StateActionType
): StateState => {
  let selectedNodes: Array<INode>;
  let selectedNode: INode;
  let selectedColor: "B" | "W";

  switch (action.type) {
    case SELECT_NODE:
      selectedNode = action.payload;
      selectedNodes = [...state.selectedNodes, action.payload];
      return { ...state, selectedNodes, selectedNode };

    case SELECT_COLOR:
      if (state.selectedColor === "B") {
        selectedColor = "W";
      } else {
        selectedColor = "B";
      }
      return { ...state, selectedColor };

    default:
      return state;
  }
};
