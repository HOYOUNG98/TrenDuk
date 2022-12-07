import sqlite3
import zipfile
import os

from tqdm import tqdm
from service.parser_ import Parser
from service.type_ import Game


def mapper():

    os.mkdir("tmp/sql_shards")
    for source_file in tqdm(os.listdir("tmp/zip_shards")):
        zipped = zipfile.ZipFile("tmp/zip_shards/" + source_file)

        games, nodes = {}, {}
        for file in zipped.namelist():
            '''
                Open sgf files and process them into nodes and games instances. 
            '''
            with zipped.open(file, "r") as f_in:
                game_info, game_moves = Parser.read_bytes(f_in.read())
                game_instance = Game(game_info)

                games[game_instance.id] = game_instance

                # There are four corners
                for sequence in Parser.divide_sequences(game_moves):

                    # There may be invalid sequences
                    if not sequence:
                        continue

                    sequence_dict = Parser.parse_sequence(sequence, game_info)

                    for key, val in sequence_dict.items():
                        if key in nodes:
                            nodes[key].mergeNode(val)
                        else:
                            nodes[key] = val
        
        year = source_file.split(".")[0]
        conn = sqlite3.connect(f'tmp/sql_shards/{year}.db')
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE node (node_id VARCHAR(10) PRIMARY KEY, move VARCHAR(2) NOT NULL, color VARCHAR(1) NOT NULL, sequence_depth INT);")
        cursor.execute("CREATE TABLE is_child (parent_id VARCHAR(10) NOT NULL, child_id VARCHAR(10) NOT NULL, FOREIGN KEY (parent_id) references node(node_id), FOREIGN KEY (child_id) references node(node_id), PRIMARY KEY (parent_id, child_id));")
        cursor.execute("CREATE TABLE game (game_id VARCHAR(10) PRIMARY KEY, datetime VARCHAR(10), event VARCHAR(50), round VARCHAR(50), black_player VARCHAR(50), black_rank VARCHAR(10), white_player VARCHAR(50), white_rank VARCHAR(10), komi VARCHAR(5), result VARCHAR(10));")
        cursor.execute("CREATE TABLE node_game (node_id VARCHAR(10) NOT NULL, game_id VARCHAR(10) NOT NULL, game_depth INTEGER, FOREIGN KEY (node_id) references node(node_id), FOREIGN KEY (game_id) references game(game_id), PRIMARY KEY (node_id, game_id, game_depth));")
        
        game_rows = []
        for key, val in games.items():
            game_rows.append((val.id, val.datetime, val.event, val.round, val.black_player, val.black_rank, val.white_player, val.white_rank, val.komi, val.result))
        
        cursor.executemany('INSERT INTO game VALUES (?,?,?,?,?,?,?,?,?,?)', game_rows)

        nodes_rows, node_game_rows, children_rows = [], [], []
        for _, val in nodes.items():
            nodes_rows.append((val.id, val.move, val.color, val.sequence_depth))

            for game_id, game_depth in val.games:
                node_game_rows.append((val.id, game_id, game_depth))

            for child in val.children:
                children_rows.append((val.id, child))
            
        cursor.executemany('INSERT INTO node VALUES (?,?,?,?);', nodes_rows)
        node_game_rows = list(set(node_game_rows))
        cursor.executemany('INSERT INTO node_game VALUES (?,?,?);', node_game_rows)
        cursor.executemany('INSERT INTO is_child VALUES (?,?);', children_rows)

        conn.commit()
        cursor.close()

if __name__ == "__main__":
    mapper()