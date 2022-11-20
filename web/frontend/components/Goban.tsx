// library imports
import React, { useRef, Ref, useEffect, useState } from "react";

declare const window: any;

interface IGobanProps {
  size: number;
  moves: Array<INode>;
}

interface INode {
  color: "B" | "W";
  x: number;
  y: number;
}

export const Goban: React.FC<IGobanProps> = ({ size, moves }) => {
  const refBoard = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (refBoard && refBoard.current && !refBoard.current.innerHTML) {
      var board = new window.WGo.Board(refBoard.current, {
        width: size,
        section: {
          top: 0,
          left: 9,
          right: 0,
          bottom: 9,
        },
      });
    }

    moves.forEach((move) => {
      board.addObject({
        x: move.x,
        y: move.y,
        c: move.color === "B" ? window.WGo.B : window.WGo.W,
      });
    });

    // return () => {
    //   console.log("!");
    //   refBoard?.current?.remove();
    // };
  }, []);

  return <div ref={refBoard} />;
};
