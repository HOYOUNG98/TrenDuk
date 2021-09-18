// library imports
import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// local imports
import { WGoBoard } from "../components/WGoBoard";
import { Chart } from "../components/Chart";
import { RootState } from "../store";
import { NavBar } from "../components/NavBar";
import { HStack, Radio, RadioGroup, Wrap } from "@chakra-ui/react";
import { ReactVisDataReducer } from "../helpers/rechartConversion";
import { IReactVisData } from "../types";

const Index: React.FC = () => {
  const [yearlyPick, yearlyPickUpate] = useState<IReactVisData[]>([]);
  const [yearlyWin, yearlyWinUpdate] = useState<IReactVisData[]>([]);

  const { currentMoves, hoverPoint, selectedColor } = useSelector(
    (state: RootState) => ({
      currentMoves: state.node.currentMoves,
      hoverPoint: state.current.hoverPoint,
      selectedColor: state.current.selectedColor,
    })
  );

  useEffect(() => {
    yearlyPickUpate(
      ReactVisDataReducer(currentMoves, hoverPoint, "pick_percentage")
    );
    yearlyWinUpdate(
      ReactVisDataReducer(currentMoves, hoverPoint, "win_percentage")
    );
  }, [hoverPoint, currentMoves]);

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
          <Chart data={yearlyPick} move={hoverPoint} variant={"선택률"} />
          <Chart data={yearlyWin} move={hoverPoint} variant={"승률"} />
        </Wrap>
      </HStack>
    </>
  );
};

export default Index;
