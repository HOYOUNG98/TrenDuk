// import libraries
import axios, { AxiosResponse, AxiosError } from "axios";

// import local files
import { IGibo } from "../types";
import { store } from "../store";

// Interface of data field
interface IResponseData {
  relatedGiboArray: Array<IGibo>;
}

export function getGibos(nodeID: string) {
  axios({
    method: "POST",
    url: "getGibos",
    baseURL: process.env.REACT_APP_API_BASE_URL,
    headers: { "Content-Type": "application/json" },
    data: { nodeID },
  })
    .then((response: AxiosResponse) => {
      const responseData: IResponseData = response.data.data;

      store.dispatch({
        type: "GET_GIBOS",
        payload: responseData.relatedGiboArray,
      });
    })
    .catch((error: AxiosError) => {
      console.error("Error connecting to API", error);
    });
}
