// library imports
import React, { forwardRef, Ref, useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { getBranches } from "../api/getBranches";

// local imports
import { RootState } from "../store";

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
          dispatch({ type: "UPDATE_HOVER_POINT", payload: -1 });
        }
      });
    });

    board.addEventListener("mousemove", function (x: number, y: number) {
      const branchNodes: INode[] =
        selectedColor === "B" ? branchPoints.black : branchPoints.white;

      branchNodes.forEach((branch, i) => {
        if (branch.x === x && branch.y === y) {
          dispatch({ type: "UPDATE_HOVER_POINT", payload: i + 1 });
          return;
        }
      });
    });

    return () => {
      let boardElement: HTMLElement = document.getElementById(
        "wgoboard"
      ) as HTMLElement;
      boardElement.innerHTML = "";
    };
  }, [branchPoints, selectedColor]);
  return <Board ref={refBoard} />;
};

const Board: React.FC<{ ref: Ref<HTMLDivElement> }> = forwardRef(
  (prop, ref) => {
    return <div ref={ref} id="wgoboard"></div>;
  }
);
