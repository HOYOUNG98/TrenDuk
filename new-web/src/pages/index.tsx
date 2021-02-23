// library imports
import React from "react";
import { useSelector } from "react-redux";

// local imports
import { WGoBoard } from "../components/WGoBoard";
import { Chart } from "../components/Chart";
import { RootState } from "../store";
import {
  pickRateConversion,
  winRateConversion,
} from "../helpers/rechartConversion";
import { NavBar } from "../components/NavBar";
import { HStack, Wrap } from "@chakra-ui/react";

const Index: React.FC = () => {
  const { branchStats, hoverPoint, selectedColor } = useSelector(
    (state: RootState) => ({
      branchStats: state.node.branchStats,
      hoverPoint: state.current.hoverPoint,
      selectedColor: state.current.selectedColor,
    })
  );

  return (
    <>
      <NavBar />
      <HStack margin={5} spacing="20px">
        <Wrap>
          <WGoBoard />
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
