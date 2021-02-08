// library imports
import useAxios from "axios-hooks";
import React, { Ref, forwardRef, useEffect, useState } from "react";
import { useSelector, shallowEqual, useDispatch } from "react-redux";

// local imports
import { INode } from "../types";
import { RootState } from "../store";

declare const window: any;

export const WGoBoard: React.FC = () => {
  const [{ data, loading, error }, refetch] = useAxios({
    url: "http://localhost:8080/getBranchPoints",
    method: "POST",
  });

  const { selectedColor, hoverPoint } = useSelector(
    (state: RootState) => ({
      selectedColor: state.current.selectedColor,
      hoverPoint: state.current.hoverPoint,
    }),
    shallowEqual
  );

  const dispatch = useDispatch();

  const [selectedNodes, updateSelectedNodes] = useState([]);

  const refBoard = React.useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!data) {
      return;
    }
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

    const branchNodes = selectedColor === "B" ? data.black : data.white;

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
      const branchNodes = selectedColor === "B" ? data.black : data.white;

      branchNodes.forEach((node) => {
        if (x === node.x && y === node.y) {
          refetch();
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
  }, [data]);
  return <Board ref={refBoard} />;
};

interface BoardProps {
  ref: Ref<HTMLDivElement>;
}

const Board: React.FC<BoardProps> = forwardRef((prop, ref) => {
  return <div ref={ref} id="wgoboard"></div>;
});
