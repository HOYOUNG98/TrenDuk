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
    


# class GameInfo:
#     def __init__(self, *args, **kwargs) -> None:
        