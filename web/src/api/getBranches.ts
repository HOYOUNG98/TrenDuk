// import libraries
import axios, { AxiosResponse, AxiosError } from "axios";

// import local files
import { INode } from "../types";
import { store } from "../store";

export function getBranches(nodeID: string | null = null) {
  axios({
    method: "POST",
    url: "getBranches",
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    data: { nodeID },
  })
    .then((response: AxiosResponse) => {
      const responseData: Array<INode> = response.data.data;
      store.dispatch({
        type: "GET_BRANCH_POINTS",
        payload: responseData,
      });

      store.dispatch({
        type: "GET_BRANCH_STATS",
        payload: responseData,
      });
    })
    .catch((error: AxiosError) => {
      console.error("Error connecting to API", error);
    });
}
