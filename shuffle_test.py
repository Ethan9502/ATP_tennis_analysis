import pandas as pd
import random

df = pd.read_csv("espn_atp_rankings.csv")
player_list = df["Player"].unique().tolist()
print(player_list)
print()
random.shuffle(player_list)
print(player_list)
