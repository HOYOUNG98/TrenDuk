// library imports
import { useBreakpointValue } from "@chakra-ui/react";
import React, { forwardRef, Ref, useEffect } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { getBranches } from "../api/getBranches";

// local imports
import { RootState } from "../store";

declare const window: any;

export const WGoBoard: React.FC = () => {
  const variant: any = useBreakpointValue({ base: 300, lg: 500 });
  const { selectedColor, selectedNodes, currentMoves } = useSelector(
    (state: RootState) => ({
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
    // Initiate Board
    if (refBoard && refBoard.current) {
      var board = new window.WGo.Board(refBoard.current, {
        width: variant,
        section: {
          top: -0.1,
          left: 9,
          right: -0.1,
          bottom: 9,
        },
      });

      var coordinates = {
        // draw on grid layer
        grid: {
          draw: function (this: any, _: any, board: any) {
            var ch, t, xleft, ytop;

            this.fillStyle = "rgba(0,0,0,0.7)";
            this.textBaseline = "middle";
            this.textAlign = "center";
            this.font = `${variant / 10}` + "px " + "sans-serif";

            xleft = board.getX(board.size - 0.6);
            ytop = board.getY(-0.4);

            for (var i = 0; i < board.size; i++) {
              ch = i + "A".charCodeAt(0);
              if (ch >= "I".charCodeAt(0)) ch++;

              t = board.getY(i);
              this.fillText(i + 1, xleft, t);

              t = board.getX(i);
              this.fillText(String.fromCharCode(ch - 1), t, ytop);
            }

            this.fillStyle = "black";
          },
        },
      };
      board.addCustomObject(coordinates);
    }

    currentMoves.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: +node.move.slice(1) - 1,
        type: "MA",
        text: "X",
      });
    });

    selectedNodes.forEach((node) => {
      board.addObject({
        x: node.move[0].charCodeAt(0) - 97,
        y: +node.move.slice(1) - 1,
        c: node.color === "B" ? window.WGo.B : window.WGo.W,
      });
    });

    // To catch user's click activity
    board.addEventListener("click", function (x: number, y: number) {
      const clickedMove = String.fromCharCode(x + 97) + (y + 1);

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
      const hoveredMove = String.fromCharCode(x + 97) + (y + 1);

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
  }, [selectedColor, currentMoves, variant]);
  return <Board ref={refBoard} />;
};

const Board: React.FC<{ ref: Ref<HTMLDivElement> }> = forwardRef(
  (_prop, ref) => {
    return <div ref={ref} id="wgoboard"></div>;
  }
);
