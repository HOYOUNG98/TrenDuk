import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import {
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  Line,
  ResponsiveContainer,
} from "recharts";
import { RootState } from "../store";

interface ChartProps {}

interface IStat {
  color: string;
  id: string;
  yearlyStat: [
    {
      year: string;
      count: number;
      win: number;
      lose: number;
    }
  ];
}

interface IChart {
  year: string;
  "1": number;
  "2": number;
  "3": number;
  "4": number;
}

export const Chart: React.FC<ChartProps> = ({}) => {
  const colors = ["#4C212A", "#3A6952", "#FC814A", "#8797AF"];
  const { branchStats, selectedColor } = useSelector((state: RootState) => ({
    branchStats: state.node.branchStats,
    selectedColor: state.current.selectedColor,
  }));

  const [chartData, updateChartData] = useState<Array<IChart>>([]);

  useEffect(() => {
    var tmpChartData: Array<IChart> = [
      { year: "2014", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2015", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2016", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2017", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2018", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2019", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2020", "1": 0, "2": 0, "3": 0, "4": 0 },
      { year: "2021", "1": 0, "2": 0, "3": 0, "4": 0 },
    ];
    var stat: Array<IStat> =
      selectedColor === "B" ? branchStats.black : branchStats.white;

    stat.forEach((branch, i) => {
      branch.yearlyStat.forEach((stat) => {
        tmpChartData.forEach((data) => {
          if (stat.year === data.year) {
            data[i + 1] = stat.count;
          }
        });
      });
    });

    updateChartData(tmpChartData);
  }, [branchStats, selectedColor]);
  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={chartData}>
        <Tooltip wrapperStyle={{ width: 100 }} />
        <XAxis dataKey="year" />
        <YAxis width={30} />
        {[1, 2, 3, 4].map((i) => {
          return <Line key={i} dataKey={i} type="linear" stroke={colors[i]} />;
        })}
      </LineChart>
    </ResponsiveContainer>
  );
};
