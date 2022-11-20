// library imports
import { Flex } from "@chakra-ui/react";
import React, { useRef, Ref, useEffect, useState } from "react";
import { AreaChart, XAxis, YAxis, Area } from "recharts";
import { Goban } from "./Goban";

const PercentChart = () => {
  const data = [
    {
      month: "2015.01",
      a: 10,
    },
    {
      month: "2015.02",
      a: 8,
    },
    {
      month: "2015.03",
      a: 9,
    },
    {
      month: "2015.04",
      a: 5,
    },
    {
      month: "2015.05",
      a: 40,
    },
    {
      month: "2015.06",
      a: 50,
    },
    {
      month: "2015.07",
      a: 66,
    },
  ];

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
      <Area type="monotone" dataKey="a" stroke="#000000" fill="#000000" />
    </AreaChart>
  );
};

export const ChildStats: React.FC<{}> = () => {
  return (
    <Flex>
      <Goban size={150} moves={[]} />
      <Flex direction={"column"}>
        <PercentChart />
        <PercentChart />
      </Flex>
    </Flex>
  );
};
