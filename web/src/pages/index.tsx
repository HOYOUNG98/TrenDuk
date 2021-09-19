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

interface IMoveData {
  move: string;
  numWin: number;
  numData: number;
  numTotal: number;
}

const Index: React.FC = () => {
  const [yearlyPick, yearlyPickUpate] = useState<IReactVisData[]>([]);
  const [yearlyWin, yearlyWinUpdate] = useState<IReactVisData[]>([]);
  const [uniqueMoves, uniqueMovesupdate] = useState<IMoveData[]>([]);

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
    var uniqueMoves: Array<IMoveData> = unique.map((move) => {
      const obj = { move, numWin: 0, numData: 0, numTotal: 0 };
      return obj;
    });
    currentMoves.forEach((move) => {
      uniqueMoves.forEach((unique) => {
        if (unique.move === move.move) {
          unique.numWin += move.num_win;
          unique.numData += move.num_data;
          unique.numTotal += move.num_total;
        }
      });
    });

    uniqueMovesupdate(uniqueMoves);
  }, [currentMoves]);

  return (
    <Flex direction="column">
      <NavBar />
      <Flex
        width="100%"
        height={["", "", "100%", "100%"]}
        marginTop={["40px", "40px", "50px", "50px"]}
        justifyContent="center"
        alignItems="center"
        direction={["column", "column", "row", "row"]}
      >
        {/* Moves List */}
        <Flex
          width={["500px", "500px", "160px", "160px"]}
          height={["80px", "80px", "500px", "500px"]}
          direction={["row", "row", "column", "column"]}
          marginRight={["0", "0", "10px", "10px"]}
          marginBottom={["10px", "10px", "0", "0"]}
          overflowX={{ base: "auto" }}
          overflowY={{ md: "auto" }}
          overflow="auto"
        >
          {uniqueMoves.map((move) => {
            return (
              <Move
                move={move.move}
                pick={+((move.numData / move.numTotal) * 100).toFixed(2)}
                win={+((move.numWin / move.numData) * 100).toFixed(2)}
                key={move.move}
              />
            );
          })}
        </Flex>
        {/* Board */}
        <WGoBoard />
        {/* Charts */}
        <Flex
          width={["500px", "500px", "40%", "40%"]}
          height={["300px", "300px", "500px", "500px"]}
          direction={["row", "row", "column", "column"]}
          marginTop={["10px", "10px", "0", "0"]}
          overflowY={{ base: "auto" }}
          marginLeft={{ md: "10px" }}
          overflowX={{ md: "auto" }}
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
