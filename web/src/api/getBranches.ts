// import libraries
import axios, { AxiosResponse, AxiosError } from "axios";

// import local files
import { INode } from "../types";
import { store } from "../cache";

// Interface of data field
interface IResponseData {
  blackChildrenNodes: Array<INode>;
  whiteChildrenNodes: Array<INode>;
}

export function getBranches(nodeID: string | null = null) {
  axios({
    method: "POST",
    url: "getBranches",
    baseURL: process.env.REACT_APP_API_BASE_URL,
    data: { nodeID },
  })
    .then((response: AxiosResponse) => {
      const responseData: IResponseData = response.data.data;
      store.dispatch({
        type: "GET_BLACK_BRANCH_NODES",
        payload: responseData.blackChildrenNodes,
      });
      store.dispatch({
        type: "GET_WHITE_BRANCH_NODES",
        payload: responseData.whiteChildrenNodes,
      });
    })
    .catch((error: AxiosError) => {
      console.error("Error connecting to API", error);
    });
}
