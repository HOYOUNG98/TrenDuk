import { INodeStats as INode } from "../store/node/types";

interface IChartData {
  [key: string]: string | number;
}

interface ITmpCountStore {
  [key: string]: number;
}

export const pickRateConversion = (
  branchStats: { black: Array<INode>; white: Array<INode> },
  selectedColor: string
): object[] => {
  const stats: Array<INode> =
    selectedColor === "B" ? branchStats.black : branchStats.white;

  var chartData: Array<IChartData> = [
    { year: "2014" },
    { year: "2015" },
    { year: "2016" },
    { year: "2017" },
    { year: "2018" },
    { year: "2019" },
    { year: "2020" },
    { year: "2021" },
  ];

  var countStore: ITmpCountStore = {
    "2014": 0,
    "2015": 0,
    "2016": 0,
    "2017": 0,
    "2018": 0,
    "2019": 0,
    "2020": 0,
    "2021": 0,
  };
  stats.forEach((stat) => {
    stat.yearlyStat.forEach((yearly) => {
      countStore[yearly.year] += yearly.count;
    });
  });

  stats.forEach((stat, i) => {
    stat.yearlyStat.forEach((year1) => {
      chartData.forEach((year2) => {
        if (year2.year == year1.year) {
          year2[i + 1] = ((year1.count / countStore[year1.year]) * 100).toFixed(
            2
          );
        }
      });
    });
  });

  return chartData;
};

export const winRateConversion = (
  branchStats: { black: Array<INode>; white: Array<INode> },
  selectedColor: string
): object[] => {
  const stats: Array<INode> =
    selectedColor === "B" ? branchStats.black : branchStats.white;

  var chartData: Array<IChartData> = [
    { year: "2014" },
    { year: "2015" },
    { year: "2016" },
    { year: "2017" },
    { year: "2018" },
    { year: "2019" },
    { year: "2020" },
    { year: "2021" },
  ];

  stats.forEach((stat, i) => {
    stat.yearlyStat.forEach((year1) => {
      chartData.forEach((year2) => {
        if (year2.year == year1.year) {
          if (year1.count == 0) {
            return;
          }
          if (year1.win !== undefined) {
            year2[i + 1] = ((year1.win / year1.count) * 100).toFixed(2);
          } else if (year1.lose !== undefined) {
            year2[i + 1] = (
              ((year1.count - year1.lose) / year1.count) *
              100
            ).toFixed(2);
          } else {
            return;
          }
        }
      });
    });
  });

  return chartData;
};