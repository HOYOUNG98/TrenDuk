// library imports
import React from "react";
import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// local imports

interface ChartProps {
  chartData: object[];
  variant: string;
  move: string;
}

export const Chart: React.FC<ChartProps> = ({ chartData, move }) => {
  console.log(chartData, move);
  return (
    <ResponsiveContainer width="100%" height={250}>
      <ComposedChart data={chartData} margin={{ top: 20, left: 20, right: 20 }}>
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
        <CartesianGrid stroke="#f5f5f5" />
        <Bar dataKey={move} barSize={20} fill="#413ea0" />
        <Line type="monotone" dataKey={move} stroke="#ff7300" />
      </ComposedChart>
    </ResponsiveContainer>
  );
};
