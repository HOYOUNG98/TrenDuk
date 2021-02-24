import {
  CurrentState,
  CurrentActionType,
  SELECT_NODE,
  SELECT_COLOR,
  UPDATE_HOVER_POINT,
} from "./types";
import { INode } from "../../types";

const initState: CurrentState = {
  selectedNode: null,
  selectedNodes: [],
  selectedColor: "B",
  hoverPoint: "",
};

export const currentReducer = (
  state = initState,
  action: CurrentActionType
): CurrentState => {
  let selectedNodes: Array<INode>;
  let selectedNode: INode;
  let selectedColor: "B" | "W";
  let hoverPoint: string;

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

    case UPDATE_HOVER_POINT:
      hoverPoint = action.payload;
      return { ...state, hoverPoint };

    default:
      return state;
  }
};
