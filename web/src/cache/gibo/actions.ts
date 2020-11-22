import { IGibo } from "../../types";
import { GET_GIBOS } from "./types";

export const getGibos = (gibos: Array<IGibo>) => ({
  type: GET_GIBOS,
  payload: gibos,
});
