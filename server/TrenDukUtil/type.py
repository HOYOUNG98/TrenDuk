from __future__ import annotations

class TreeNode:
    def __init__(self, move:str, color:str, depth:int, game_id:int) -> None:
        self.id: int = hash((move, color, depth))
        self.move = move
        self.color = color
        self.depth = depth
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


class GameInfo:
    def __init__(self, game_id) -> None:
        self.id = game_id