// library imports
import React, { forwardRef, Ref, useEffect } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { getBranches } from "../api/getBranches";

// local imports
import { RootState } from "../store";

declare const window: any;

export const WGoBoard: React.FC = () => {
  const { branchPoints, selectedColor, selectedNodes, currentMoves } =
    useSelector(
      (state: RootState) => ({
        branchPoints: state.node.branchPoints,
        selectedColor: state.current.selectedColor,
        selectedNodes: state.current.selectedNodes,
        currentMoves: state.node.currentMoves,
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
    console.log(selectedNodes);
    // Initiate Board
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

    currentMoves.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
        type: "LB",
        text: "X",
      });
    });

    selectedNodes.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
        c: node.color === "B" ? window.WGo.B : window.WGo.W,
      });
    });

    // To catch user's click activity
    board.addEventListener("click", function (x: number, y: number) {
      const clickedMove =
        String.fromCharCode(x + 97) + String.fromCharCode(y + 97);

      currentMoves.forEach((node) => {
        if (node.move === clickedMove) {
          var color: "B" | "W" = selectedColor === "W" ? "B" : "W";
          getBranches(node.depth + 1, node._id, color);
          dispatch({ type: "SELECT_NODE", payload: node });
          dispatch({ type: "SELECT_COLOR" });
        }
      });
    });

    // To catch user's hovering activity
    board.addEventListener("mousemove", function (x: number, y: number) {
      const hoveredMove =
        String.fromCharCode(x + 97) + String.fromCharCode(y + 97);
      currentMoves.forEach((node) => {
        if (node.move === hoveredMove) {
          dispatch({ type: "UPDATE_HOVER_POINT", payload: node.move });
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
  }, [branchPoints, selectedColor, currentMoves]);
  return <Board ref={refBoard} />;
};

const Board: React.FC<{ ref: Ref<HTMLDivElement> }> = forwardRef(
  (_prop, ref) => {
    return <div ref={ref} id="wgoboard"></div>;
  }
);
