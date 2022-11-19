// library imports
import React, { forwardRef, Ref, useEffect, useState } from "react";

declare const window: any;

export const Goban: React.FC = () => {
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

    return () => {
      let boardElement: HTMLElement = document.getElementById(
        "wgoboard"
      ) as HTMLElement;
      boardElement.innerHTML = "";
    };
  }, []);
  return <Board ref={refBoard} />;
};

const Board: React.FC<{ ref: Ref<HTMLDivElement> }> = forwardRef(
  (_prop, ref) => {
    return <div ref={ref} id="wgoboard"></div>;
  }
);
