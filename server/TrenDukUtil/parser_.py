from __future__ import annotations
from type_ import TreeNode, GameInfo

class Parser:
    @staticmethod
    def read_bytes(file: str) -> tuple[str, list[str]]:
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
    def parse_sequence(sequence: list[str], game_info: str) -> dict[int, 'TreeNode']:
        
        res: dict[int, 'TreeNode'] = {}
        sequence = Parser.align_sequence(sequence)
        root = TreeNode.root()

        game_instance = GameInfo(game_info)

        for idx, move in enumerate(sequence):
            color, coordinate, game_depth = move[0], move[2:4], move[5:]
            move_instance = TreeNode(coordinate, color, idx+1, int(game_depth), game_instance.id)
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

            if x < 'i' and y < 'i':
                top_left.append(move + depth)
            elif x < 'i' and y > 'i':
                bottom_left.append(move + depth)
            elif x > 'i' and y < 'i':
                top_right.append(move + depth)
            elif x > 'i' and y > 'i':
                bottom_right.append(move + depth)

        return [top_left, bottom_left, top_right, bottom_right]
    
    @staticmethod
    def align_sequence(sequence: list[str]) -> list[str]:
        first_move = sequence[0]
        first_move_x, first_move_y = first_move[2:4][0], first_move[2:4][1]

        # Allow sequence to be in top right corner
        if first_move_x > 'i' or first_move_y > 'i':
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
            
            new_x = x if x > 'i' else chr(ord('s') - ord(x) + ord('a'))
            new_y = y if y > 'i' else chr(ord('s') - ord(y) + ord('a'))

            sequence[idx] = move[:2] + new_x + new_y + move[4:]
        
        # reflect by moves
        first_non_axis_move: str | None = None
        for move in sequence:
            x, y = move[2:4][0], move[2:4][1]
            if x != y:
               first_non_axis_move = move
        
        if not first_non_axis_move:
            raise ValueError
        
        for idx, move in enumerate(sequence):
            x, y = move[2:4][0], move[2:4][1]

            sequence[idx] = move[:2] + y + x + move[4:]
        
        return sequence