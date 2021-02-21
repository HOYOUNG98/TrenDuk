// library imports
import useAxios from "axios-hooks";
import React, { Ref, forwardRef, useEffect, useState } from "react";
import { useSelector, shallowEqual, useDispatch } from "react-redux";

// local imports
import { RootState } from "../store";
import { getBranches } from "../api/getBranches";
import { getGibos } from "../api/getGibos";

interface INode {
  id: string;
  x: number;
  y: number;
  color: "B" | "W";
}

declare const window: any;

export const WGoBoard: React.FC = () => {
  const [selectedNodes, updateSelectedNodes] = useState<INode[]>([]);

  const { branchPoints, selectedColor, hoverPoint, branchStats } = useSelector(
    (state: RootState) => ({
      branchPoints: state.node.branchPoints,
      selectedColor: state.current.selectedColor,
      hoverPoint: state.current.hoverPoint,
      branchStats: state.node.branchStats,
    }),
    shallowEqual
  );
  console.log(branchStats);

  const dispatch = useDispatch();

  const refBoard = React.useRef<HTMLDivElement>(null);

  // Wait for API request - API request when render
  useEffect(() => {
    getBranches();
  }, []);

  useEffect(() => {
    if (refBoard && refBoard.current) {
      var board = new window.WGo.Board(refBoard.current, {
        width: 500,
        section: {
          top: 0,
          left: 9,
          right: 0,
          bottom: 9,
        },
      });
    }

    const branchNodes: INode[] =
      selectedColor === "B" ? branchPoints.black : branchPoints.white;

    branchNodes.forEach((node, i) => {
      board.addObject({
        x: node.x,
        y: node.y,
        type: "LB",
        text: i + 1,
      });
    });

    selectedNodes.forEach((node) => {
      board.addObject({
        x: node.x,
        y: node.y,
        c: node.color === "B" ? window.WGo.B : window.WGo.W,
      });
    });

    board.addEventListener("click", function (x: number, y: number) {
      const branchNodes: INode[] =
        selectedColor === "B" ? branchPoints.black : branchPoints.white;

      branchNodes.forEach((node) => {
        if (x === node.x && y === node.y) {
          getBranches(node.id);
          updateSelectedNodes([...selectedNodes, node]);
          dispatch({ type: "SELECT_COLOR" });
        }
      });
    });

    return () => {
      let boardElement: HTMLElement = document.getElementById(
        "wgoboard"
      ) as HTMLElement;
      boardElement.innerHTML = "";
    };
  }, [branchPoints]);
  return <Board ref={refBoard} />;
};

const Board: React.FC<{ ref: Ref<HTMLDivElement> }> = forwardRef(
  (prop, ref) => {
    return <div ref={ref} id="wgoboard"></div>;
  }
);
