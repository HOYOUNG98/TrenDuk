import React from "react";
import { useSelector, shallowEqual } from "react-redux";
import {
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  Line,
  ResponsiveContainer,
} from "recharts";

interface ChartProps {}

export const Chart: React.FC<ChartProps> = ({}) => {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={graphData}>
        <Tooltip wrapperStyle={{ width: 100 }} />
        <XAxis dataKey="year" />
        <YAxis width={30} />
        {keySet.map((key, i) => {
          return (
            <Line
              key={key}
              dataKey={key}
              type="linear"
              stroke={colors[i]}
              strokeWidth={hoverPoint === key ? 3 : 1}
            />
          );
        })}
      </LineChart>
    </ResponsiveContainer>
  );
};
