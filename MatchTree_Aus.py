import pandas as pd
import random
from MatchNode import *

player_df = pd.read_csv("dataset/modified_espn_atp_rankings.csv")
player_df = player_df[player_df["Player"] != "Echargui M."]
current_player_list = player_df["Player"].tolist()
current_player_list = current_player_list[0: 128]
random.shuffle(current_player_list)

round_type = {'1st Round': 0, '2nd Round': 1, 'Quarterfinals': 2, 'Semifinals': 3, 
              'The Final': 4, '3rd Round': 5, '4th Round': 6, 'Round Robin': 7}
round_sequence = ["1st Round", "2nd Round", "3rd Round", "4th Round", "Quarterfinals", "Semifinals", "The Final"]

print(current_player_list)
print("-----------------------------")
for round in round_sequence:
    winner_list = []
    for i in range(0, len(current_player_list), 2):
        match = GameMatchNode(current_player_list[i], current_player_list[i + 1], 3, 1, 2, round_type[round], "2025-11-23")
        match.deter_winner()
        winner_list.append(match.winner)
    current_player_list = winner_list
    print(winner_list)

