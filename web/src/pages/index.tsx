// library imports
import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// local imports
import { WGoBoard } from "../components/WGoBoard";
import { Chart } from "../components/Chart";
import { RootState } from "../store";
import { NavBar } from "../components/NavBar";
import { HStack, Radio, RadioGroup, Wrap } from "@chakra-ui/react";
import { IYearlyReChartData } from "../types";
import { ReChartYearlyDataReducer } from "../helpers/rechartConversion";

const Index: React.FC = () => {
  const [yearlyPick, yearlyPickUpate] = useState<IYearlyReChartData[]>([]);
  const [yearlyWin, yearlyWinUpdate] = useState<IYearlyReChartData[]>([]);

  const { currentYearlyPick, currentYearlyWin, hoverPoint, selectedColor } =
    useSelector((state: RootState) => ({
      currentYearlyPick: state.node.currentYearlyPick,
      currentYearlyWin: state.node.currentYearlyWin,
      currentMoves: state.node.currentMoves,
      hoverPoint: state.current.hoverPoint,
      selectedColor: state.current.selectedColor,
    }));

  useEffect(() => {
    yearlyPickUpate(ReChartYearlyDataReducer(currentYearlyPick, hoverPoint));
    yearlyWinUpdate(ReChartYearlyDataReducer(currentYearlyWin, hoverPoint));
  }, [hoverPoint, currentYearlyPick, currentYearlyWin]);

  const dispatch = useDispatch();
  return (
    <>
      <NavBar />
      <HStack margin={5} spacing="20px">
        <Wrap>
          <WGoBoard />
          <RadioGroup
            value={selectedColor === "B" ? "1" : "2"}
            onChange={() => {
              dispatch({ type: "SELECT_COLOR" });
            }}
          >
            <HStack spacing={5}>
              <Radio colorScheme="black" value="1">
                흑
              </Radio>
              <Radio colorScheme="white" value="2">
                백
              </Radio>
            </HStack>
          </RadioGroup>
        </Wrap>
        <Wrap marginRight="20px">
          <Chart chartData={yearlyPick} move={hoverPoint} variant={"선택률"} />
          <Chart chartData={yearlyWin} move={hoverPoint} variant={"승률"} />
        </Wrap>
      </HStack>
    </>
  );
};

export default Index;
