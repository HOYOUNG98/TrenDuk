from __future__ import annotations

class TreeNode:
    def __init__(self, move:str, color:str, sequence_depth:int, game_depth: int, game_id:int) -> None:
        self.id: int = hash((move, color, sequence_depth))
        self.move = move
        self.color = color
        self.sequence_depth = sequence_depth
        self.game_depth = game_depth
        self.games: list[int] = [game_id]
        self.children: set[int] = set()
    
    def mergeNode(self, other: 'TreeNode') -> None:
        if self.id != other.id:
            raise ValueError
        
        self.games.extend(other.games)
        self.children.update(other.children)
    
    def addChild(self, node_id:int) -> None:
        self.children.add(node_id)
    
    def existsChild(self, node_id:int) -> bool:
        return node_id in self.children
    
    @classmethod
    def root(cls):
        return cls('root', 'root', 0, 0, -1)
    
    def __repr__(self):
        return self.color + self.move
    


class GameInfo:
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
        
        self.id = hash((self.black_player, self.white_player, self.datetime, self.event))
    
    def __repr__(self):
        return f"{self.black_player}({self.black_rank}) vs {self.white_player}({self.white_rank}), {self.result}, {self.datetime}"