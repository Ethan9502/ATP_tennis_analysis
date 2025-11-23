import pandas as pd
import pickle

player_info = pd.read_csv("espn_atp_rankings.csv")
tennis_df = pd.read_csv("/Users/chiangethan/.cache/kagglehub/datasets/dissfya/atp-tennis-2000-2023daily-pull/versions/911/atp_tennis.csv")

with open("model/logistic.pkl", "rb") as f:
    log_model = pickle.load(f)

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

class GameMatchNode:
    def __init__(self, player_1, player_2, series, court, surface, round, right = None, left = None):
        self.player_1 = player_1
        self.player_2 = player_2
        self.series = series
        self.court = court
        self.surface = surface
        self.round = round
        self.right = right
        self.left = left
        self.winner = None
    
    def deter_winner(self):
        p1_df = player_info[player_info["Player"] == self.player_1]
        p2_df = player_info[player_info["Player"] == self.player_2]
        rank_diff = p1_df["Rank"].iloc[0] - p2_df["Rank"].iloc[0]
        pts_diff = p1_df["Points"].iloc[0] - p2_df["Points"].iloc[0]
        odds_diff = 0
        
        input_df = pd.DataFrame({})
        

        return winner