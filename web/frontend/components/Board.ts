const BOARD_SIZE = 19;

enum Color {
  EMPTY = 0,
  BLACK = 1,
  WHITE = 2,
}

interface IMove {
  x: number;
  y: number;
}

export class Board {
  current_color: number;
  board: Array<Array<number>>;

  constructor() {
    this.current_color = Color.BLACK;
    this.board = Array<Array<number>>(BOARD_SIZE).fill(
      Array<number>(BOARD_SIZE).fill(Color.EMPTY)
    );
  }

  switchPlayer() {
    this.current_color =
      this.current_color == Color.BLACK ? Color.WHITE : Color.BLACK;
  }

  play(move: IMove) {
    var { x, y } = move;

    if (this.board[x][y] !== Color.EMPTY) {
      return false;
    }

    this.board[x][y] = this.current_color;
    this.switchPlayer();
    return true;
  }
}
