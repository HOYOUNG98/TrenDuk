// import libraries
import axios, { AxiosResponse, AxiosError } from "axios";

// import local files
import { store } from "../store";

export async function getBranches(
  move: string | null = null,
  parent: string | "root" = "root",
  color: "B" | "W" = "B"
) {
  await axios({
    method: "GET",
    url: "getBranches",
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    params: { move, parent, color },
  })
    .then((response: AxiosResponse) => {
      const responseData = response.data.branches;
      let winRateData = [];
      let pickRateData = [];
      let currentMoves = new Set<string>();
      for (let i = 0; i < responseData.length; i++) {
        const yearly = responseData[i];
        let yearlyData1: any = { year: yearly[0]["year"] };
        let yearlyData2: any = { year: yearly[0]["year"] };
        for (let j = 0; j < yearly.length; j++) {
          const move = yearly[j];
          yearlyData1[move.move] = move.win_percentage;
          yearlyData2[move.move] = move.pick_percentage;
          currentMoves.add(move.move);
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
