// library imports
import React, { useEffect } from "react";
import { useSelector, shallowEqual, useDispatch } from "react-redux";
import { Radio } from "antd";

// local imports
import { getBranches } from "../api/getBranches";
import { getGibos } from "../api/getGibos";
import { RootState } from "../cache";
import { INode } from "../types";

declare const window: any;

export const Board = () => {
  const {
    blackBranchNodes,
    whiteBranchNodes,
    selectedNodes,
    selectedColor,
  } = useSelector(
    (state: RootState) => ({
      blackBranchNodes: state.node.blackBranchNodes,
      whiteBranchNodes: state.node.whiteBranchNodes,
      selectedNodes: state.state.selectedNodes,
      selectedColor: state.state.selectedColor,
    }),
    shallowEqual
  );

  const dispatch = useDispatch();

  // Wait for API request - API request when render
  useEffect(() => {
    getBranches();
  }, []);

  // Rendering board
  useEffect(() => {
    renderBoard();
    return () => {
      let boardElement: HTMLElement = document.getElementById(
        "wgoboard"
      ) as HTMLElement;
      boardElement.innerHTML = "";
    };
  }, [selectedColor, selectedNodes, blackBranchNodes, whiteBranchNodes]);

  const renderBoard = () => {
    var board = new window.WGo.Board(document.getElementById("wgoboard"), {
      width: 500,
      section: {
        top: 0,
        left: 9,
        right: 0,
        bottom: 9,
      },
    });

    let boardElement: HTMLElement = document.getElementById(
      "wgoboard"
    ) as HTMLElement;

    boardElement.style.margin = "0";

    var branchNodes: Array<INode>;
    if (selectedColor === "B") {
      branchNodes = blackBranchNodes;
    } else {
      branchNodes = whiteBranchNodes;
    }

    // add labels
    branchNodes.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
        type: "LB",
        text: node.move,
      });
    });

    // add already selected stones
    selectedNodes.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
        c: node.color === "B" ? window.WGo.B : window.WGo.W,
      });
    });

    board.addEventListener("click", function (x: number, y: number) {
      const branchNodes =
        selectedColor === "B" ? blackBranchNodes : whiteBranchNodes;

      for (var i = 0; i < branchNodes.length; i++) {
        if (
          branchNodes[i].move[0].charCodeAt(0) - 97 === x &&
          branchNodes[i].move[1].charCodeAt(0) - 97 === y
        ) {
          getBranches(branchNodes[i]._id);
          getGibos(branchNodes[i]._id);
          dispatch({ type: "SELECT_NODE", payload: branchNodes[i] });
          dispatch({ type: "SELECT_COLOR" });
        }
      }
    });
  };

  return (
    <div style={{ display: "table-cell", verticalAlign: "middle" }}>
      <div
        style={{ height: "80%", width: "80%", padding: "0 0 10px" }}
        id="wgoboard"
      ></div>
      <Radio.Group
        value={selectedColor}
        onChange={() => dispatch({ type: "SELECT_COLOR" })}
        size="middle"
      >
        <Radio.Button value="B">Black</Radio.Button>
        <Radio.Button value="W">White</Radio.Button>
      </Radio.Group>
    </div>
  );
};
