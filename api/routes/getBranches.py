class GetBranchesAPI(Resource):
    def get():
        filenames = listdir("../../data/moves")

        depth = request.args.get("depth", default=0, type=int)
        parent = request.args.get("parent", default="root", type=str)
        color = request.args.get("color", default="B", type=str)

        branches = []
        filenames.sort()
        for file in filenames:
            nodes_df = read_csv("./data/moves/" + file)

            # change id type to str
            nodes_df["_id"] = nodes_df["_id"].astype(str)

            popular_moves = nodes_df.loc[
                (nodes_df["depth"] == depth) & (nodes_df["parent"] == parent) & (nodes_df["color"] == color)
            ].sort_values(by=["num_data"], ascending=False)[:5]
            popular_moves["num_total"] = popular_moves["num_data"].sum()

            # get win percentage
            popular_moves["win_percentage"] = round(popular_moves["num_win"] / popular_moves["num_data"] * 100, 1)

            # get pick percentage
            popular_moves["pick_percentage"] = round(popular_moves["num_data"] / popular_moves["num_total"] * 100, 1)

            popular_moves = popular_moves.loc[popular_moves["num_data"] > 10]
            popular_moves = popular_moves.drop(columns=["link", "parent"])
            popular_moves["year"] = file[:4]

            branches.append(popular_moves.to_dict("records"))

        if len([inner for outer in branches for inner in outer]) == 0:
            return {"status": 200, "message": "no moves meets given criteria"}

        return {"status": 200, "branches": branches}