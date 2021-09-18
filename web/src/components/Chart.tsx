// library imports
import React from "react";
import {
  XYPlot,
  VerticalBarSeries,
  HorizontalGridLines,
  VerticalGridLines,
  XAxis,
  YAxis,
} from "react-vis";
import { IReactVisData } from "../types";

// local imports

interface ChartProps {
  data: Array<IReactVisData>;
  variant: string;
  move: string;
}

export const Chart: React.FC<ChartProps> = ({ data }) => {
  return (
    <div>
      <XYPlot
        height={300}
        width={800}
        yDomain={[0, 100]}
        xDomain={[2007.8, 2021.2]}
      >
        <VerticalBarSeries data={data} barWidth={0.5} color={"black"} />
        <XAxis />
        <YAxis />
        <HorizontalGridLines />
        <VerticalGridLines />
      </XYPlot>
    </div>
  );
};
