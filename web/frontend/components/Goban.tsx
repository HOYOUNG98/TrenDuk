// library imports
import React, { useRef, useEffect, useState } from "react";

declare const window: any;

interface IGobanProps {
  size: number;
  moves: Array<IMove>;
}

interface IMove {
  color: "B" | "W";
  x: number;
  y: number;
}

export const Goban: React.FC<IGobanProps> = ({ size, moves }) => {
  const refBoard = useRef<HTMLDivElement>(null);
  const [board, setBoard] = useState<any>(null);

  useEffect(() => {
    if (refBoard && refBoard.current && !refBoard.current.innerHTML) {
      var initBoard = new window.WGo.Board(refBoard.current, {
        width: size,
        section: {
          top: 0,
          left: 10,
          right: 0,
          bottom: 10,
        },
      });

      setBoard(initBoard);

      moves.forEach((move) => {
        initBoard.addObject({
          x: move.x,
          y: move.y,
          c: move.color === "B" ? window.WGo.B : window.WGo.W,
        });
      });
    }

    // return () => {
    //   console.log("!");
    //   refBoard?.current?.remove();
    // };
  });

  useEffect(() => {
    if (board) {
      board.removeAllObjects();
      moves.forEach((move) => {
        board.addObject({
          x: move.x,
          y: move.y,
          c: move.color === "B" ? window.WGo.B : window.WGo.W,
        });
      });
    }
  }, [moves]);

  return <div ref={refBoard} />;
};
