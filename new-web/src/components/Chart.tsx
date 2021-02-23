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
  hoverPoint: number;
  variant: string;
}

export const Chart: React.FC<ChartProps> = ({
  chartData,
  hoverPoint,
  variant,
}) => {
  const colors = ["#4C212A", "#3A6952", "#FC814A", "#8797AF"];

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

        <Legend />
        {[1, 2, 3, 4].map((i) => {
          return (
            <Line
              name={`${i}번 ${variant}`}
              dataKey={i}
              key={i}
              type="linear"
              stroke={colors[i]}
              strokeWidth={hoverPoint === i ? 3 : 1}
            />
          );
        })}
      </LineChart>
    </ResponsiveContainer>
  );
};
