// library imports
import { Flex } from "@chakra-ui/react";
import React, { Dispatch, SetStateAction } from "react";
import { AreaChart, Area } from "recharts";
import { colorObjToStr } from "../utils/helper";
import { Goban } from "./Goban";

interface IPercentChartProps {
  data: Array<any>;
}

interface IMove {
  color: "B" | "W";
  x: number;
  y: number;
  depth: number;
}

interface IChildStatsProps {
  pickRate: Array<any>;
  winRate: Array<any>;
  moves: Array<IMove>;
  updateNode: Dispatch<SetStateAction<string>>;
  updateMoves: Dispatch<SetStateAction<IMove[]>>;
}

const PercentChart: React.FC<IPercentChartProps> = ({ data }) => {
  return (
    <AreaChart
      width={250}
      height={75}
      data={data}
      stackOffset="expand"
      margin={{
        top: 10,
        right: 30,
        left: 0,
        bottom: 0,
      }}
    >
      <Area type="monotone" dataKey="rate" stroke="#000000" fill="#000000" />
    </AreaChart>
  );
};

export const ChildStats: React.FC<IChildStatsProps> = ({
  pickRate,
  winRate,
  moves,
  updateNode,
}) => {
  const handleBoardClick = () => {
    updateNode(colorObjToStr(moves[moves.length - 1]));
  };
  return (
    <Flex gap={3}>
      <div onClick={handleBoardClick}>
        <Goban size={150} moves={moves} />
      </div>
      <Flex direction={"column"}>
        <PercentChart data={pickRate} />
        <PercentChart data={winRate} />
      </Flex>
    </Flex>
  );
};
