from __future__ import annotations
from uuid import UUID


class Node:
    def __init__(self, move: str, color: str, sequence_depth: int, game_depth: int, game_id: str, parent_id: str) -> None:
        self.id: str = f'{move}{color}{sequence_depth}{parent_id}'
        self.move = move
        self.color = color
        self.sequence_depth = sequence_depth
        self.games: list[list[str | int]] = [[game_id, game_depth]]
        self.children: set[str] = set()

    def mergeNode(self, other: 'Node') -> None:
        if self.id != other.id:
            raise ValueError

        self.games.extend(other.games)
        self.children.update(other.children)

    def addChild(self, node_id: str) -> None:
        self.children.add(node_id)

    def existsChild(self, node_id: int) -> bool:
        return node_id in self.children

    @classmethod
    def root(cls):
        return cls('root', 'root', 0, 0, 'root', 'root')

    def __repr__(self):
        return self.color + self.move

    def as_dict(self):
        dict_val = self.__dict__
        dict_val["children"] = list(self.children)

        return dict_val

    @classmethod
    def keys(cls):
        return ["id", "move", "color", "sequence_depth", "games", "children"]


class Game:
    def __init__(self, *args) -> None:
        default_info: dict[str, None | str] = {
            'DT': None,
            'EV': None,
            'RO': None,
            'PB': None,
            'BR': None,
            'PW': None,
            'WR': None,
            'KM': None,
            'RE': None,
        }

        if len(args) == 1 and isinstance(args[0], str):
            for val in args[0].split("]"):
                key: str = val[:2]
                if key in default_info:
                    default_info[key] = val[3:]

        self.datetime = default_info['DT']
        self.event = default_info['EV']
        self.round = default_info['RO']
        self.black_player = default_info['PB']
        self.black_rank = default_info['BR']
        self.white_player = default_info['PW']
        self.white_rank = default_info['WR']
        self.komi = default_info['KM']
        self.result = default_info['RE']

        self.id: str = f'{self.black_player}{self.white_player}{self.datetime}{self.event}'

    def __repr__(self):
        return f"{self.black_player}({self.black_rank}) vs {self.white_player}({self.white_rank}), {self.result}, {self.datetime}"

    @classmethod
    def keys(cls):
        return cls.__dict__.keys()
