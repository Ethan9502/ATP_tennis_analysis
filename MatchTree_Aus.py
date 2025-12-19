import pandas as pd
import random
from MatchNode import *

class MatchTree:
    def __init__(self):
        self.root = None

player_df = pd.read_csv("dataset/modified_espn_atp_rankings.csv")
player_df = player_df[player_df["Player"] != "Echargui M."]
current_player_list = player_df["Player"].tolist()
current_player_list = current_player_list[0: 128]
random.shuffle(current_player_list)

round_type = {'1st Round': 0, '2nd Round': 1, 'Quarterfinals': 2, 'Semifinals': 3, 
              'The Final': 4, '3rd Round': 5, '4th Round': 6, 'Round Robin': 7}
round_sequence = ["1st Round", "2nd Round", "3rd Round", "4th Round", "Quarterfinals", "Semifinals", "The Final"]

player_winning_time = {}
time = 0
print(current_player_list)
print("-----------------------------")

for i in range(1000):
    instance = current_player_list
    for round in round_sequence:
        winner_list = []
        for i in range(0, len(instance), 2):
            match = GameMatchNode(instance[i], instance[i + 1], 3, 1, 2, round_type[round], "2025-11-23")
            match.deter_winner()
            winner_list.append(match.winner)
        instance = winner_list
    tree = MatchTree()
    tree.root = instance[0]
    if instance[0] not in player_winning_time.keys():
        player_winning_time[instance[0]] = 1
    else:
        player_winning_time[instance[0]] += 1
    time += 1
    print(time)
    random.shuffle(current_player_list)

sorted_items = sorted(player_winning_time.items(), key=lambda item: item[1])
sorted_dict = dict(sorted_items)
print(sorted_dict)


