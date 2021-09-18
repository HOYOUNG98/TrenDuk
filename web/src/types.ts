export interface IGibo {
  _id: string;
  giboName: string;
  giboDate: string;
  giboLocation?: string;
  giboMinutes?: number;
  giboSeconds?: number;
  giboTimeCount?: number;
  giboKomi?: number;
  giboResult?: string;
  giboBlackPlayerName: string;
  giboBlackPlayerRank?: string;
  giboWhitePlayerName: string;
  giboWhitePlayerRank?: string;
  giboMoves?: Array<string>;
  giboLink?: string;
  published?: Date;
  analyzed?: boolean;
}

export interface INode {
  _id: string;
  depth: number;
  move: string;
  color: "B" | "W";
}

export interface IYearlyNode extends INode {
  pick_percentage: number;
  win_percentage: number;
  year: number;
}

export interface IReactVisData {
  x: number;
  y: number;
}
