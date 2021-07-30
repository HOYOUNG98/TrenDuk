// library imports
import React from "react";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// local imports
import { INode } from "../types";

interface ChartProps {
  chartData: object[];
  hoverPoint: string;
  variant: string;
  moves: Array<INode>;
}

export const Chart: React.FC<ChartProps> = ({ chartData, moves }) => {
  const arrayMoves = Array.from(moves);

  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={chartData} margin={{ top: 20, left: 20, right: 20 }}>
        <Tooltip
          itemSorter={(item) => {
            return (item.value as number) * -1;
          }}
        />
        <XAxis dataKey="year" />
        <YAxis
          width={30}
          tickFormatter={(tick) => {
            return `${tick}%`;
          }}
        />

        {arrayMoves.map((move) => {
          return (
            <Line
              dataKey={move.move}
              key={move._id}
              type="linear"
              stroke={"#888488"}
              strokeWidth={3}
            />
          );
        })}
      </LineChart>
    </ResponsiveContainer>
  );
};
