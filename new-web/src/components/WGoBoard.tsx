// library imports
import useAxios from "axios-hooks";
import React, { Ref, forwardRef, useEffect, useState } from "react";
import { useSelector, shallowEqual, useDispatch } from "react-redux";

// local imports
import { INode } from "../types";
import { RootState } from "../store";

declare const window: any;

export const WGoBoard: React.FC = () => {
  const [{ data, loading, error }, refetch] = useAxios(
    "http://localhost:4000/getBranches"
  );

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

    branchNodes.forEach((node) => {
      board.addObject({
        x: node.x,
        y: node.y,
        type: "LB",
        text: node.move,
      });
    });

    selectedNodes.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
        c: node.color === "B" ? window.WGo.B : window.WGo.W,
      });
    });

    board.addEventListener("click", function (x: number, y: number) {
      const branchNodes = selectedColor === "B" ? data.black : data.white;

      for (var i = 0; i < branchNodes.length; i++) {
        if (
          branchNodes[i].move[0].charCodeAt(0) - 97 === x &&
          branchNodes[i].move[1].charCodeAt(0) - 97 === y
        ) {
          refetch();
          updateSelectedNodes([...selectedNodes, branchNodes[i]]);
          dispatch({ type: "SELECT_COLOR" });
        }
      }
    });
  }, [refBoard, data, selectedNodes]);
  return <Board ref={refBoard} />;
};

interface BoardProps {
  ref: Ref<HTMLDivElement>;
}

const Board: React.FC<BoardProps> = forwardRef((prop, ref) => {
  return <div ref={ref}></div>;
});
