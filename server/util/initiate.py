from __future__ import annotations
from os import listdir
from parser_ import Parser
from tqdm import tqdm
from type_ import Node, Game

if __name__ == "__main__":
    files = listdir("./data/raw/")
    
    nodes: dict[str, 'Node'] = {}
    games: dict[str, 'Game'] = {}
    for file in tqdm(files[:5000]):
        game_info, game_moves = Parser.read_bytes("./data/raw/" + file)
        game_instance = Game(game_info)

        games[game_instance.id] = game_instance

        for sequence in Parser.divide_sequences(game_moves):
            
            if not sequence:
                continue
            
            sequence_dict = Parser.parse_sequence(sequence, game_info)

            for key, val in sequence_dict.items():
                if key in nodes:
                    nodes[key].mergeNode(val)
                else:
                    nodes[key] = val

    
    with open('./initiate.sql', 'w') as file:

        file.write("PRAGMA journal_mode = OFF;")
        file.write("PRAGMA synchronous = 0;")
        file.write("PRAGMA locking_mode = EXCLUSIVE;")
        file.write("PRAGMA temp_store = MEMORY;")

        file.write("CREATE TABLE node (node_id VARCHAR(10) PRIMARY KEY, move VARCHAR(2) NOT NULL, color VARCHAR(1) NOT NULL, sequence_depth INT); \n")
        file.write("CREATE TABLE game (game_id VARCHAR(10) PRIMARY KEY, datetime VARCHAR(10), event VARCHAR(50), round VARCHAR(50), black_player VARCHAR(50), black_rank VARCHAR(10), white_player VARCHAR(50), white_rank VARCHAR(10), komi VARCHAR(5), result VARCHAR(10)); \n")
        file.write("CREATE TABLE node_game (node_id VARCHAR(10) NOT NULL, game_id VARCHAR(10) NOT NULL, game_depth INTEGER, FOREIGN KEY (node_id) references node(node_id), FOREIGN KEY (game_id) references game(game_id), PRIMARY KEY (node_id, game_id, game_depth)); \n")
        file.write("CREATE TABLE is_child (parent_id VARCHAR(10) NOT NULL, child_id VARCHAR(10) NOT NULL, FOREIGN KEY (parent_id) references node(node_id), FOREIGN KEY (child_id) references node(node_id), PRIMARY KEY (parent_id, child_id)); \n")

        for key, val in games.items():
            file.write(f'INSERT INTO game VALUES ("{val.id}", "{val.datetime}", "{val.event}", "{val.round}", "{val.black_player}", "{val.black_rank}", "{val.white_player}", "{val.white_rank}", "{val.komi}", "{val.result}"); \n')

        for key, val in nodes.items():
            file.write(f'INSERT INTO node VALUES ("{val.id}", "{val.move}", "{val.color}", {val.sequence_depth}); \n')

            for game_id, game_depth in val.games:
                file.write(f'INSERT INTO node_game VALUES ("{val.id}", "{game_id}", "{game_depth}"); \n')
            
            for child in val.children:
                file.write(f'INSERT INTO is_child VALUES ("{val.id}", "{child}"); \n')
                