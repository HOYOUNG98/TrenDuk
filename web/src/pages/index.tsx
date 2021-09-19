// library imports
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Flex } from "@chakra-ui/react";

// local imports
import { WGoBoard } from "../components/WGoBoard";
import { Chart } from "../components/Chart";
import { RootState } from "../store";
import { NavBar } from "../components/NavBar";
import { ReactVisDataReducer } from "../helpers/rechartConversion";
import { IReactVisData } from "../types";
import { Move } from "../components/Move";

const Index: React.FC = () => {
  const [yearlyPick, yearlyPickUpate] = useState<IReactVisData[]>([]);
  const [yearlyWin, yearlyWinUpdate] = useState<IReactVisData[]>([]);
  const [uniqueMoves, uniqueMovesupdate] = useState<string[]>([]);

  const { currentMoves, hoverPoint } = useSelector((state: RootState) => ({
    currentMoves: state.node.currentMoves,
    hoverPoint: state.current.hoverPoint,
  }));

  useEffect(() => {
    yearlyPickUpate(
      ReactVisDataReducer(currentMoves, hoverPoint, "pick_percentage")
    );
    yearlyWinUpdate(
      ReactVisDataReducer(currentMoves, hoverPoint, "win_percentage")
    );
  }, [hoverPoint, currentMoves]);

  useEffect(() => {
    const unique = [...new Set(currentMoves.map((item) => item.move))];
    uniqueMovesupdate(unique);
  }, [currentMoves]);

  return (
    <Flex direction="column">
      <NavBar />
      <Flex
        width="100%"
        height="100%"
        marginTop="-50px"
        justifyContent="center"
        alignItems="center"
        direction={["column", "column", "row", "row"]}
      >
        {/* Moves List */}
        <Flex
          width={["100%", "160px", "160px", "160px"]}
          height={["100px", "500px", "500px", "500px"]}
          direction={["row", "row", "column", "column"]}
          marginRight={"10px"}
          overflowX="auto"
        >
          {uniqueMoves.map((move) => {
            return <Move move={move} pick={50} win={50} />;
          })}
        </Flex>
        {/* Board */}
        <WGoBoard />
        {/* Charts */}
        <Flex
          width={["100%", "40%", "40%", "40%"]}
          height={["100px", "500px", "500px", "500px"]}
          direction={["row", "row", "column", "column"]}
          MarginLeft={"10px"}
          overflow="auto"
        >
          <Chart
            data={yearlyPick}
            move={hoverPoint}
            variant={"Pick Rate (%)"}
          />
          <Chart data={yearlyWin} move={hoverPoint} variant={"Win Rate (%)"} />
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Index;
