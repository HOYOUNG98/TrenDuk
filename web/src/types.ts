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
  root?: boolean;
  parentID: string;
  childrenID?: Array<string>;
  move: string;
  color: string;
  games?: Array<string>;
  yearlyStat: Array<YearlyStat>;
}

interface YearlyStat {
  year: string;
  count: number;
  win?: number;
  lose?: number;
}
