// library imports
import React from "react";
import { useSelector, useDispatch } from "react-redux";

// local imports
import { WGoBoard } from "../components/WGoBoard";
import { Chart } from "../components/Chart";
import { RootState } from "../store";
import {
  pickRateConversion,
  winRateConversion,
} from "../helpers/rechartConversion";
import { NavBar } from "../components/NavBar";
import { HStack, Radio, RadioGroup, Wrap } from "@chakra-ui/react";

const Index: React.FC = () => {
  const { branchStats, hoverPoint, selectedColor } = useSelector(
    (state: RootState) => ({
      branchStats: state.node.branchStats,
      hoverPoint: state.current.hoverPoint,
      selectedColor: state.current.selectedColor,
    })
  );

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
          <Chart
            chartData={pickRateConversion(branchStats, selectedColor)}
            hoverPoint={hoverPoint}
            variant={"선택률"}
          />
          <Chart
            chartData={winRateConversion(branchStats, selectedColor)}
            hoverPoint={hoverPoint}
            variant={"승률"}
          />
        </Wrap>
      </HStack>
    </>
  );
};

export default Index;
