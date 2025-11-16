import pandas as pd
import matplotlib.pyplot as plt

tennis_df = pd.read_csv("/Users/chiangethan/.cache/kagglehub/datasets/dissfya/atp-tennis-2000-2023daily-pull/versions/911/atp_tennis.csv")
tennis_df["Date"] = pd.to_datetime(tennis_df["Date"])

def ranking_plt(name):
    player_record = tennis_df[(tennis_df["Player_1"] == name) | (tennis_df["Player_2"] == name)]
    player_rank = pd.DataFrame({"Date": [], "Rank": []})
    for i in range(len(player_record)):
        if player_record.iloc[i]["Player_1"] == "Alcaraz C.":
            player_rank.loc[i, "Date"] = player_record.iloc[i]["Date"]
            player_rank.loc[i, "Rank"] = player_record.iloc[i]["Rank_1"]
        else:
            player_rank.loc[i, "Date"] = player_record.iloc[i]["Date"]
            player_rank.loc[i, "Rank"] = player_record.iloc[i]["Rank_2"]

    date = player_rank["Date"]
    rank = player_rank["Rank"]
    plt.figure(figsize = (20, 6))
    plt.plot(date, rank)
    for i in range(0, len(date), 20):
        plt.text(date[i], rank[i], f'({date[i].month}, {rank[i]})', fontsize=8, ha='center', va='bottom')
    plt.show()

ranking_plt("Alcaraz C.")