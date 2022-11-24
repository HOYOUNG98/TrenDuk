// library imports
import { Flex } from "@chakra-ui/react";
import React, { useRef, Ref, useEffect, useState } from "react";
import { AreaChart, XAxis, YAxis, Area } from "recharts";
import { Goban } from "./Goban";

interface IPercentChartProps {
  data: Array<any>;
}

interface IMove {
  color: "B" | "W";
  x: number;
  y: number;
}

interface IChildStatsProps {
  pickRate: Array<any>;
  winRate: Array<any>;
  moves: Array<IMove>;
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
}) => {
  return (
    <Flex gap={3}>
      <Goban size={150} moves={moves} />
      <Flex direction={"column"}>
        <PercentChart data={pickRate} />
        <PercentChart data={winRate} />
      </Flex>
    </Flex>
  );
};
