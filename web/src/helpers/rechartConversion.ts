import { IReactVisData, IYearlyNode } from "../types";

export const ReactVisDataReducer = (
  currentMoves: Array<IYearlyNode>,
  hoverPoint: string,
  key: "pick_percentage" | "win_percentage"
) => {
  var result: Array<IReactVisData> = [];
  var newArr = currentMoves.filter((node) => node.move === hoverPoint);
  newArr.forEach((node) => {
    result.push({ x: node.year, y: node[key] });
  });

  return result;
};
