// library imports
import React from "react";
import {
  HorizontalGridLines,
  VerticalGridLines,
  XAxis,
  YAxis,
  FlexibleWidthXYPlot,
  LineSeries,
  ChartLabel,
} from "react-vis";

// local imports
import { IReactVisData } from "../types";

interface ChartProps {
  data: Array<IReactVisData>;
  variant: string;
  move: string;
}

const referenceData = [...Array(14).keys()].map((i) => {
  return { x: 2008 + i, y: 50 };
});

export const Chart: React.FC<ChartProps> = ({ data, variant }) => {
  return (
    <div>
      <FlexibleWidthXYPlot
        height={300}
        yDomain={[0, 100]}
        xDomain={[2008, 2021]}
      >
        <XAxis />
        <YAxis />
        <HorizontalGridLines />
        <VerticalGridLines />
        <LineSeries data={data} color={"black"} style={{ strokeWidth: 1 }} />
        <LineSeries
          data={referenceData}
          color={"8f8f8f"}
          strokeStyle={"dashed"}
        />
        <ChartLabel
          text="Year"
          className="alt-x-label"
          includeMargin={false}
          xPercent={0.025}
          yPercent={1.01}
        />

        <ChartLabel
          text={variant}
          className="alt-y-label"
          includeMargin={false}
          xPercent={0.03}
          yPercent={0.06}
          style={{
            transform: "rotate(-90)",
            textAnchor: "end",
          }}
        />
      </FlexibleWidthXYPlot>
    </div>
  );
};
