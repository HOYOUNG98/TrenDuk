from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

if __name__ == "__main__":
    games_df = read_csv("./data/games/cleaned_all_games.csv")
    games_df.dropna(subset=["PWR", "OWR", "AWR"], inplace=True)

    feature_cols = [
        "PL5G",
        "OL5G",
        "PS",
        "OS",
        "PWR",
        "OWR",
        "AWR",
    ]

    X = games_df[feature_cols]
    y = games_df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    accuracy = metrics.accuracy_score(y_test, y_pred)

    print("CONFUSION MATRIX:", cnf_matrix)
    print("ACCURACY:", accuracy)
