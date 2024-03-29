from __future__ import annotations
from service.type_ import Node, Game


class Parser:
    @staticmethod
    def read_file(file: str) -> tuple[str, list[str]]:
        res = ""
        with open(file, "rb") as f:
            byte = f.read(1)
            while byte != b"":
                res += byte.decode("utf-8")
                byte = f.read(1)

        res = res.replace("\n", "").replace("(", "").replace(")", "")[1:]
        res = res.split(";")

        return res[0], res[1:]

    @staticmethod
    def read_bytes(_bytes: str):

        res = _bytes.decode("utf-8")
        res = res.replace("\n", "").replace("(", "").replace(")", "")[1:]
        res = res.split(";")

        return res[0], res[1:]

    @staticmethod
    def parse_sequence(sequence: list[str], game_info: str) -> dict[str, 'Node']:
        res: dict[str, 'Node'] = {}
        sequence = Parser.align_sequence(sequence)
        root = Node.root()

        game_instance = Game(game_info)

        for idx, move in enumerate(sequence):
            color, coordinate, game_depth = move[0], move[2:4], move[5:]

            # We don't want to compute all the way
            if int(game_depth) > 9:
                continue
            
            move_instance = Node(coordinate, color, idx+1,
                                 int(game_depth), game_instance.id, root.id)
            root.addChild(move_instance.id)
            root = move_instance

            res[move_instance.id] = move_instance

        return res

    @staticmethod
    def divide_sequences(moves: list[str]) -> list[list[str]]:
        top_left = []
        top_right = []
        bottom_left = []
        bottom_right = []

        # Skip the root node which has general information of game.
        # Start looking at moves.
        for idx, move in enumerate(moves):

            x, y = move[2:4][0], move[2:4][1]
            depth = str(idx+1)

            if x < 'j' and y < 'j':
                top_left.append(move + depth)
            elif x < 'j' and y > 'j':
                bottom_left.append(move + depth)
            elif x > 'j' and y < 'j':
                top_right.append(move + depth)
            elif x > 'j' and y > 'j':
                bottom_right.append(move + depth)

        return [top_left, bottom_left, top_right, bottom_right]

    @staticmethod
    def align_sequence(sequence: list[str]) -> list[str]:
        first_move = sequence[0]
        first_move_x, first_move_y = first_move[2:4][0], first_move[2:4][1]

        # Allow sequence to be in top right corner
        try:
            sequence = Parser.reflect_sequence(sequence)
        except ValueError:
            return []

        return sequence

    @staticmethod
    def reflect_sequence(sequence: list[str]) -> list[str]:

        # reflect by corners
        for idx, move in enumerate(sequence):
            x, y = move[2:4][0], move[2:4][1]

            new_x = x if x > 'j' else chr(ord('s') - ord(x) + ord('a'))
            new_y = y if y > 'j' else chr(ord('s') - ord(y) + ord('a'))

            sequence[idx] = move[:2] + new_x + new_y + move[4:]

        # reflect by moves
        first_non_axis_move: str | None = None
        for move in sequence:
            x, y = move[2:4][0], move[2:4][1]
            if x != y:
                first_non_axis_move = move
                break

        if not first_non_axis_move:
            raise ValueError

        if first_non_axis_move[2:4][0] > first_non_axis_move[2:4][1]:
            for idx, move in enumerate(sequence):
                x, y = move[2:4][0], move[2:4][1]

                sequence[idx] = move[:2] + y + x + move[4:]

        return sequence
