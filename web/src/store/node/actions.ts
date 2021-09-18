import { INode } from "../../types";
import { GET_CURRENT_MOVES } from "./types";

export const getCurrentMoves = (moves: Array<INode>) => ({
  type: GET_CURRENT_MOVES,
  payload: moves,
});
