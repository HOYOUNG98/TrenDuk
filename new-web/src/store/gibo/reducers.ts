import { GiboState, GiboActionTypes, GET_GIBOS } from "./types";
import { IGibo } from "../../types";

const initState: GiboState = {
  gibos: [],
};

export const giboReducer = (
  state = initState,
  action: GiboActionTypes
): GiboState => {
  let gibos: Array<IGibo>;

  switch (action.type) {
    case GET_GIBOS:
      gibos = action.payload;
      return { ...state, gibos };
    default:
      return state;
  }
};
