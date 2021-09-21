// import libraries
import axios, { AxiosResponse, AxiosError } from "axios";

// import local files
import { store } from "../store";
import { IYearlyNode } from "../types";

export async function getBranches(
  depth: number | null = 0,
  parent: string | "root" = "root",
  color: "B" | "W" = "B"
) {
  await axios({
    method: "GET",
    url: "getBranches",
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    params: { depth, parent, color },
  })
    .then((response: AxiosResponse) => {
      const responseData: Array<Array<IYearlyNode>> = response.data.branches;
      var newArr: Array<IYearlyNode> = [];
      newArr = newArr.concat(...responseData);
      store.dispatch({
        type: "GET_CURRENT_MOVES",
        payload: newArr,
      });
    })
    .catch((error: AxiosError) => {
      console.error("Error connecting to API", error);
    });
}
