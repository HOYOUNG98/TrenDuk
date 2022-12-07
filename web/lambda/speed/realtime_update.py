import sqlite3
import zipfile
import sys
import boto3

from service.parser_ import Parser
from service.type_ import Game
from datetime import date

OUT_BUCKET_NAME = "trenduk-speed"

def main(zip_path):
    conn = sqlite3.connect("../api/realtime_view.db")
    cursor = conn.cursor()

    res = cursor.execute("SELECT node_id FROM precomputed;")
    id_set = set(map(lambda x: x[0], res.fetchall()))

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for sgf_file in zip_file.namelist():

            # Invalid SGF files
            if sgf_file.split(".")[-1] != "sgf":
                continue

            data = zip_file.read(sgf_file)

            try:
                game_info, game_moves = Parser.read_bytes(data)
            except:
                continue

            game_instance = Game(game_info)

            year = game_instance.datetime[:4]
            winner = game_instance.result[0]

            for sequence in Parser.divide_sequences(game_moves):

                # They may be invalid sequences
                if not sequence:
                    continue

                sequence_dict = Parser.parse_sequence(sequence, game_info)

                for key, val in sequence_dict.items():

                    if key not in id_set:
                        continue
                    
                    query = f"""
                        UPDATE precomputed 
                        SET 
                            pick_rate_numerator{year} = pick_rate_numerator{year} + 1,
                            pick_rate_denominator{year} = pick_rate_denominator{year} + 1,
                            win_rate_numerator{year} = win_rate_numerator{year} + {1 if winner == val.color else 0},
                            win_rate_denominator{year} = win_rate_denominator{year} + 1
                        WHERE
                            node_id = "{key}";
                    """

                    cursor.execute(query)
        conn.commit()
        cursor.close()

    s3_client = boto3.client('s3')
    s3_client.upload_file(f"../api/realtime_view.db", OUT_BUCKET_NAME, f"{date.today()}.db")
            
            
if __name__ == "__main__":
    zip_path = sys.argv[1]
    main(zip_path)