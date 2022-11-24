interface IMove {
  color: "B" | "W";
  x: number;
  y: number;
  depth: number;
}

export const colorStrToObj = (str: string): IMove => {
  const color = str.substring(2, 3) as "B" | "W";
  const x = str.substring(0).charCodeAt(0) - "a".charCodeAt(0);
  const y = 18 - (str.substring(1).charCodeAt(0) - "a".charCodeAt(0));
  const depth = parseInt(str.substring(3));

  return { color, x, y, depth };
};

export const colorObjToStr = (obj: IMove): string => {
  const x = String.fromCharCode(obj.x + "a".charCodeAt(0));
  const y = String.fromCharCode(18 - obj.y + "a".charCodeAt(0));

  return `${x}${y}${obj.color}${obj.depth}`;
};
