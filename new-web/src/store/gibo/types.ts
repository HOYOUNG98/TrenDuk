import { IGibo } from "../../types";

export interface GiboState {
  gibos: Array<IGibo>;
}

export const GET_GIBOS = "GET_GIBOS";

interface getGibosAction {
  type: typeof GET_GIBOS;
  payload: Array<IGibo>;
}

export type GiboActionTypes = getGibosAction;
