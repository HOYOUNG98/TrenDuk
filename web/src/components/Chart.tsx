import React from "react";
import {
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface ChartProps {
  chartData: object[];
  hoverPoint: string;
  variant: string;
  moves: Set<string>;
}

export const Chart: React.FC<ChartProps> = ({
  chartData,
  hoverPoint,
  moves,
  variant,
}) => {
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
              dataKey={move}
              key={move}
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
