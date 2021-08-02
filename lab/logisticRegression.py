from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

if __name__ == "__main__":
    games_df = read_csv("./data/games/cleaned_all_games.csv")
    games_df["label"] = 1
    games_df["wwinrate"] = games_df["wnumwin"] / (games_df["wnumwin"] + games_df["wnumlose"])
    games_df["lwinrate"] = games_df["lnumwin"] / (games_df["lnumwin"] + games_df["lnumlose"])

    games_df.dropna(subset=["wwinrate", "lwinrate"], inplace=True)

    feature_cols = [
        "wlast5games",
        "llast5games",
        "wstreak",
        "lstreak",
        "wagainstwin",
        "lagainstwin",
        "wwinrate",
        "lwinrate",
    ]

    X = games_df[feature_cols]

    y = games_df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    print(cnf_matrix)
