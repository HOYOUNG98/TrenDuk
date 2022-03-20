from __future__ import annotations
from os import listdir
from parser_ import Parser
from tqdm import tqdm
from type_ import TreeNode

if __name__ == "__main__":
    files = listdir("./data/raw/")
    
    res: dict[int, 'TreeNode'] = {}
    for file in tqdm(files):
        game_info, game_moves = Parser.read_bytes("./data/raw/"+file)

        for sequence in Parser.divide_sequences(game_moves):
            
            if not sequence:
                continue
            
            sequence_dict = Parser.parse_sequence(sequence, game_info)

            for key, val in sequence_dict.items():
                if key in res:
                    res[key].mergeNode(val)
                else:
                    res[key] = val
    
    
    with open('./create_db.sql', 'a') as file:
        for key, val in res.items():
            file.write(f"INSERT INTO node VALUES ({val.id}, '{val.move}', '{val.color}', {val.sequence_depth}, {val.games}, {list(val.children)}); \n")
