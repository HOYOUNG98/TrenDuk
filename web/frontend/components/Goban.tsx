// library imports
import React, { useRef, Ref, useEffect, useState } from "react";

declare const window: any;

interface IGobanProps {
  size: number;
}

export const Goban: React.FC<IGobanProps> = ({ size }) => {
  const refBoard = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (refBoard && refBoard.current && !refBoard.current.innerHTML) {
      new window.WGo.Board(refBoard.current, {
        width: size,
        section: {
          top: 0,
          left: 9,
          right: 0,
          bottom: 9,
        },
      });
    }

    // return () => {
    //   console.log("!");
    //   refBoard?.current?.remove();
    // };
  }, []);

  return <div ref={refBoard} />;
};
