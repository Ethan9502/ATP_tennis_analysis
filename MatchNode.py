import pandas as pd
import pickle

player_info = pd.read_csv("dataset/espn_atp_rankings.csv")
tennis_df = pd.read_csv("/Users/chiangethan/.cache/kagglehub/datasets/dissfya/atp-tennis-2000-2023daily-pull/versions/911/atp_tennis.csv")
individual_record_df = pd.read_csv("dataset/individual_record_df.csv")

with open("model/logistic.pkl", "rb") as f:
    log_model = pickle.load(f)

with open("model/random_forest.pkl", "rb") as f:
    random_fr = pickle.load(f)

def head_to_head(p1, p2, date):
    past_match = tennis_df[
        (((tennis_df["Player_1"] == p1) | (tennis_df["Player_1"] == p2)) & 
        ((tennis_df["Player_2"] == p1) | (tennis_df["Player_2"] == p2))) & 
        (tennis_df["Date"] < date)
    ].tail(1)
    if len(past_match) == 0:
        return None
    winner = past_match["Winner"].iloc[0]
    return winner

def find_last_10_game(name, date):
    past_record = individual_record_df[(individual_record_df["Player"] == name) & (individual_record_df["Date"] < date)]
    if len(past_record) == 0:
        return 0.5
    if len(past_record) < 10:
        win_game = len(past_record[past_record["Status"] == "win"])
        number_of_game = len(past_record)
        adj_win_rate = (win_game + 5 * 0.5) / (number_of_game + 5)
        return adj_win_rate
    past_10 = past_record.tail(10)
    win_percentage = len(past_10[past_10["Status"] == "win"]) / 10
    return win_percentage

class GameMatchNode:
    def __init__(self, player_1, player_2, series, court, surface, round, date, right = None, left = None):
        self.player_1 = player_1
        self.player_2 = player_2
        self.series = series
        self.court = court
        self.surface = surface
        self.round = round
        self.date = date
        self.right = right
        self.left = left
        self.winner = None

    def __str__(self):
        return self.winner
    
    def deter_winner(self):
        p1_df = player_info[player_info["Player"] == self.player_1]
        p2_df = player_info[player_info["Player"] == self.player_2]
        rank_diff = p1_df["Rank"].iloc[0] - p2_df["Rank"].iloc[0]
        pts_diff = p1_df["Points"].iloc[0] - p2_df["Points"].iloc[0]
        odds_diff = 0

        p1_head_record = None
        p2_head_record = None
        last_time_winner = head_to_head(self.player_1, self.player_2, self.date)
        if last_time_winner == self.player_1:
            p1_head_record = 1
            p2_head_record = -1
        elif last_time_winner == self.player_2:
            p1_head_record = -1
            p2_head_record = 1
        else: 
            p1_head_record = 0
            p2_head_record = 0

        p1_last_10_percentage = find_last_10_game(self.player_1, self.date)
        p1_input_df = pd.DataFrame([{"rank_diff": rank_diff, "pts_diff": pts_diff, "odds_diff": odds_diff, 
                                 "series": self.series, "court": self.court, "surface": self.surface, 
                                 "round": self.round, "head_to_head": p1_head_record, "last_10_percent": p1_last_10_percentage}])
        p1_proba = random_fr.predict_proba(p1_input_df)[0, 1]

        p2_last_10_percentage = find_last_10_game(self.player_2, self.date)
        p2_input_df = pd.DataFrame([{"rank_diff": rank_diff, "pts_diff": pts_diff, "odds_diff": odds_diff, 
                                 "series": self.series, "court": self.court, "surface": self.surface, 
                                 "round": self.round, "head_to_head": p2_head_record, "last_10_percent": p2_last_10_percentage}])
        p2_proba = random_fr.predict_proba(p2_input_df)[0, 1]

        if p1_proba > p2_proba:
            self.winner = self.player_1
        else:
            self.winner = self.player_2


# node = GameMatchNode('Jarry N.', 'Sinner J.', 3, 1, 2, 4, "2025-11-23")
# node.deter_winner()
# print(node.winner)


