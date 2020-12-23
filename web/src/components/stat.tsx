// library imports
import React, { useState, useEffect } from "react";
import { useSelector, shallowEqual } from "react-redux";
import {
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  Line,
  ResponsiveContainer,
} from "recharts";
import { Table } from "antd";

// local imports
import { RootState } from "../cache";
import { IGibo, INode } from "../types";

export const RateStat = () => {
  const { blackBranchNodes, whiteBranchNodes, selectedColor } = useSelector(
    (state: RootState) => ({
      blackBranchNodes: state.node.blackBranchNodes,
      whiteBranchNodes: state.node.whiteBranchNodes,

      selectedColor: state.state.selectedColor,
    }),
    shallowEqual
  );

  const [graphData, setGraphData] = useState<Array<any>>([]);
  const [keySet, setKeySet] = useState<Array<string>>([]);
  const colors = ["#4C212A", "#3A6952", "#FC814A", "#8797AF"];

  useEffect(() => {
    if (selectedColor === "B") {
      convertToGraphDataFormat(blackBranchNodes);
    } else {
      convertToGraphDataFormat(whiteBranchNodes);
    }
  }, [blackBranchNodes, whiteBranchNodes, selectedColor]);

  const convertToGraphDataFormat = (data: Array<INode>) => {
    var graphData = [
      { year: "2014" },
      { year: "2015" },
      { year: "2016" },
      { year: "2017" },
      { year: "2018" },
      { year: "2019" },
      { year: "2020" },
    ];
    var keys = new Set();
    data.forEach((node) => {
      var nodeStat = node.yearPickCount;
      var nodeMove = node.move;
      graphData.forEach((data: any) => {
        if (Object.keys(nodeStat).indexOf(data.year) !== -1) {
          data[nodeMove] = nodeStat[data.year];
          keys.add(nodeMove);
        }
      });
    });

    for (var i = 0; i < graphData.length; i++) {
      const { year, ...rest }: any = graphData[i];
      let sum = 0;
      Object.keys(rest).forEach((key) => (sum += rest[key]));
      Object.keys(rest).forEach(
        (key) => (rest[key] = (rest[key] / sum).toFixed(2))
      );
      graphData[i] = { year, ...rest };
    }
    setGraphData(graphData);
    var keysArray = Array.from(keys) as Array<string>;
    setKeySet(keysArray);
  };

  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={graphData}>
        <Tooltip wrapperStyle={{ width: 100 }} />
        <XAxis dataKey="year" />
        <YAxis width={30} />
        {keySet.map((key, i) => {
          return (
            <Line key={key} dataKey={key} type="monotone" stroke={colors[i]} />
          );
        })}
      </LineChart>
    </ResponsiveContainer>
  );
};

/*
  Table Component
*/

interface ITableData {
  key: string;
  title: string;
  black: string;
  white: string;
  date: string;
}

interface ITableColumn {
  title: string;
  dataIndex: string;
  key: string;
}

export const GiboTable = () => {
  const { gibos } = useSelector((state: RootState) => ({
    gibos: state.gibo.gibos,
  }));

  const [tableData, updateData] = useState<Array<ITableData>>([]);
  const [tableColumn, updateColumn] = useState<Array<ITableColumn>>([]);

  useEffect(() => {
    var tempData: Array<ITableData> = [];
    gibos.forEach((gibo: IGibo) => {
      var data: ITableData = {
        key: gibo._id,
        title: gibo.giboName,
        black: gibo.giboBlackPlayerName,
        white: gibo.giboWhitePlayerName,
        date: gibo.giboDate,
      };
      tempData.push(data);
    });
    updateData(tempData);

    var tempColumn = [
      {
        title: "Title",
        dataIndex: "title",
        key: "title",
      },
      {
        title: "Black",
        dataIndex: "black",
        key: "black",
      },
      {
        title: "White",
        dataIndex: "white",
        key: "white",
      },
      {
        title: "Date",
        dataIndex: "date",
        key: "date",
      },
    ];
    updateColumn(tempColumn);
  }, [gibos]);

  return (
    <Table
      dataSource={tableData}
      columns={tableColumn}
      pagination={{ position: ["bottomCenter"], pageSize: 5 }}
    />
  );
};

/*

*/
