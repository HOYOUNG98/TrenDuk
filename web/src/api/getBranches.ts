// import libraries
import axios, { AxiosResponse, AxiosError } from "axios";

// import local files
import { store } from "../store";
import { INode, IYearlyNode, IYearlyReChartData } from "../types";

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
      console.log(responseData);
      let winRateData: Array<IYearlyReChartData> = [];
      let pickRateData: Array<IYearlyReChartData> = [];
      let currentMoves = Array<INode>();
      for (let i = 0; i < responseData.length; i++) {
        const yearly = responseData[i];
        let yearlyData1: IYearlyReChartData;
        let yearlyData2: IYearlyReChartData;
        if (yearly.length === 0) {
          yearlyData1 = { year: 2008 + i };
          yearlyData2 = { year: 2008 + i };
        } else {
          yearlyData1 = { year: yearly[0]["year"] };
          yearlyData2 = { year: yearly[0]["year"] };
        }
        for (let j = 0; j < yearly.length; j++) {
          const move = yearly[j];
          yearlyData1[move.move] = move.win_percentage;
          yearlyData2[move.move] = move.pick_percentage;
          currentMoves.push({
            move: move.move,
            _id: move._id,
            depth: move.depth,
            color: move.color,
          });
        }
        winRateData.push(yearlyData1);
        pickRateData.push(yearlyData2);
      }

      store.dispatch({
        type: "GET_CURRENT_MOVES",
        payload: currentMoves,
      });

      store.dispatch({
        type: "GET_CURRENT_YEARLY_WIN",
        payload: winRateData,
      });

      store.dispatch({
        type: "GET_CURRENT_YEARLY_PICK",
        payload: pickRateData,
      });
    })
    .catch((error: AxiosError) => {
      console.error("Error connecting to API", error);
    });
}
