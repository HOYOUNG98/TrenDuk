// library imports
import { Center, Flex } from "@chakra-ui/react";
import React, { Dispatch, SetStateAction } from "react";
import { AreaChart, Area, XAxis, YAxis } from "recharts";
import { colorObjToStr } from "../utils/helper";
import { Goban } from "./Goban";

interface IPercentChartProps {
  data: Array<any>;
  type: "pick" | "win";
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

const PercentChart: React.FC<IPercentChartProps> = ({ data, type }) => {
  return (
    <AreaChart
      width={250}
      height={75}
      data={data}
      stackOffset="expand"
      margin={{
        top: 0,
        right: 30,
        left: -10,
        bottom: 0,
      }}
    >
      <XAxis dataKey="year" domain={[2010, 2022]} />
      <YAxis domain={type == "pick" ? [0, 0.5] : [0, 1]} />
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
        <Goban size={200} moves={moves} />
      </div>
      <Flex direction={"column"}>
        <Center height="5">Pick Rate</Center>
        <PercentChart data={pickRate} type="pick" />
        <Center height="5">Win Rate</Center>
        <PercentChart data={winRate} type="win" />
      </Flex>
    </Flex>
  );
};
