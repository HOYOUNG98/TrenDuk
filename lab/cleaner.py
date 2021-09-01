from pandas import DataFrame, read_csv
import csv
from tqdm import tqdm


if __name__ == "__main__":
    # # combine all games csv
    # games_df = DataFrame()

    # for year in range(2021, 2005, -1):
    #     temp_df = read_csv("./data/games/{}_games.csv".format(year))
    #     games_df = games_df.append(temp_df)

    # print(games_df)
    # games_df.to_csv(
    #     "./data/games/all_games.csv",
    #     index=False,
    #     encoding="utf-8-sig",
    #     quotechar='"',
    #     quoting=csv.QUOTE_ALL,
    # )

    games_df = read_csv("./data/games/cleaned_all_games.csv")

    # # Add new column of win - lose of last 5 games
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df = games_df.iloc[i + 1 :].loc[
    #         (games_df["winner"] == row1["winner"]) | (games_df["loser"] == row1["winner"])
    #     ][:5]
    #     value = 0
    #     for _, row2 in filtered_df.iterrows():
    #         value = value + 1 if row1["winner"] == row2["winner"] else value - 1
    #     games_df.loc[i, "wlast5games"] = value

    # # Add new column of win - lose of last 10 games
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df = games_df.iloc[i + 1 :].loc[
    #         (games_df["winner"] == row1["loser"]) | (games_df["loser"] == row1["loser"])
    #     ][:5]
    #     value = 0
    #     for _, row2 in filtered_df.iterrows():
    #         value = value + 1 if row1["loser"] == row2["winner"] else value - 1
    #     games_df.loc[i, "llast5games"] = value

    # # Add new column of winner streak
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df = games_df.iloc[i + 1 :].loc[
    #         (games_df["winner"] == row1["winner"]) | (games_df["loser"] == row1["winner"])
    #     ]

    #     if len(filtered_df) == 0:
    #         games_df.loc[i, "wstreak"] = 0
    #         continue

    #     value = 1 if filtered_df.iloc[0]["winner"] == row1["winner"] else -1
    #     for _, row2 in filtered_df[1:].iterrows():
    #         if row1["winner"] == row2["winner"] and value > 0:
    #             value += 1
    #         elif row1["winner"] == row2["loser"] and value < 0:
    #             value -= 1
    #         else:
    #             break

    #     games_df.loc[i, "wstreak"] = value

    # # Add new column of loser streak
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df = games_df.iloc[i + 1 :].loc[
    #         (games_df["winner"] == row1["loser"]) | (games_df["loser"] == row1["loser"])
    #     ]

    #     if len(filtered_df) == 0:
    #         games_df.loc[i, "lstreak"] = 0
    #         continue

    #     value = 1 if filtered_df.iloc[0]["loser"] == row1["winner"] else -1
    #     for _, row2 in filtered_df[1:].iterrows():
    #         if row1["loser"] == row2["winner"] and value > 0:
    #             value += 1
    #         elif row1["loser"] == row2["loser"] and value < 0:
    #             value -= 1
    #         else:
    #             break

    #     games_df.loc[i, "lstreak"] = value

    # # Add new column of against
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df1 = games_df.iloc[i + 1 :].loc[
    #         ((row1["winner"] == games_df["winner"]) & (row1["loser"] == games_df["loser"]))
    #     ]
    #     filtered_df2 = games_df.iloc[i + 1 :].loc[
    #         ((row1["winner"] == games_df["loser"]) & (row1["loser"] == games_df["winner"]))
    #     ]

    #     games_df.loc[i, "wagainstwin"] = filtered_df1.shape[0]
    #     games_df.loc[i, "lagainstwin"] = filtered_df2.shape[0]

    # # Add new column of winner win percentage
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df1 = games_df.iloc[i + 1 :].loc[(row1["winner"] == games_df["winner"])]
    #     filtered_df2 = games_df.iloc[i + 1 :].loc[(row1["winner"] == games_df["loser"])]

    #     games_df.loc[i, "wnumwin"] = filtered_df1.shape[0]
    #     games_df.loc[i, "wnumlose"] = filtered_df2.shape[1]

    # # Add new column of loser win percentage
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     filtered_df1 = games_df.iloc[i + 1 :].loc[(row1["loser"] == games_df["winner"])]
    #     filtered_df2 = games_df.iloc[i + 1 :].loc[(row1["loser"] == games_df["loser"])]

    #     games_df.loc[i, "lnumwin"] = filtered_df1.shape[0]
    #     games_df.loc[i, "lnumlose"] = filtered_df2.shape[0]

    # # Reflect data to double the data

    # games_df["label"] = 1
    # new_games_df = DataFrame()
    # for i, row1 in tqdm(games_df.iterrows(), total=games_df.shape[0]):
    #     new_row = {
    #         "date": row1["date"],
    #         "player": row1["opponent"],
    #         "opponent": row1["player"],
    #         "playerlast5games": row1["opponentlast5games"],
    #         "opponentlast5games": row1["playerlast5games"],
    #         "playerstreak": row1["opponentstreak"],
    #         "opponentstreak": row1["playerstreak"],
    #         "playeragainstwin": row1["opponentagainstwin"],
    #         "opponentagainstwin": row1["playeragainstwin"],
    #         "playernumwin": row1["opponentnumwin"],
    #         "opponentnumwin": row1["playernumwin"],
    #         "playernumlose": row1["opponentnumlose"],
    #         "opponentnumlose": row1["playernumlose"],
    #         "label": 0,
    #     }
    #     new_games_df = new_games_df.append(new_row, ignore_index=True)

    # games_df = games_df.append(new_games_df)

    # change column names
    print(games_df)

    games_df = games_df.rename(
        columns={
            "playerlast5games": "PL5G",
            "opponentlast5games": "OL5G",
            "playerstreak": "PS",
            "opponentstreak": "OS",
            "playeragainstwin": "PAW",
            "opponentagainstwin": "OAW",
            "playernumwin": "PNW",
            "playernumlose": "PNL",
            "opponentnumwin": "ONW",
            "opponentnumlose": "ONL",
        }
    )

    games_df["PWR"] = games_df["PNW"] / (games_df["PNW"] + games_df["PNL"])
    games_df["OWR"] = games_df["ONW"] / (games_df["ONW"] + games_df["ONL"])
    games_df["AWR"] = games_df["PAW"] / (games_df["PAW"] + games_df["OAW"])

    games_df = games_df.loc[:, ~games_df.columns.str.contains("^Unnamed")]
    games_df.to_csv("./data/games/all_games.csv")
