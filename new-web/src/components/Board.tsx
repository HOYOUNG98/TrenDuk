import React, { Ref, forwardRef } from "react";
interface BoardProps {
  ref: Ref<HTMLDivElement>;
}

export const Board: React.FC<BoardProps> = forwardRef((prop, ref) => {
  return <div ref={ref}></div>;
});
