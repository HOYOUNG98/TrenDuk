import React, { useEffect } from "react";
import { Board } from "../components/Board";

declare const window: any;

const Index: React.FC = () => {
  const WGoboard = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (WGoboard && WGoboard.current) {
      new window.WGo.Board(WGoboard.current, {
        width: 500,
        section: {
          top: 0,
          left: 9,
          right: 0,
          bottom: 9,
        },
      });
    }
  }, [WGoboard]);
  return <Board ref={WGoboard} />;
};

export default Index;
