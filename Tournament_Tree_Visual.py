import pandas as pd
import random
from MatchNode import *
import matplotlib.pyplot as plt

class MatchTree:
    def __init__(self):
        self.root = None

    # -------- label for each match node --------
    def _label_match(self, node):
        return f"{node.player_1} vs {node.player_2}\nW: {node.winner}"

    # -------- recursive drawing helper --------
    def _draw_top_down(self, node, x, y, dx):
        if node is None:
            return

        plt.text(
            x, y, self._label_match(node),
            ha="center", va="center",
            bbox=dict(boxstyle="round", ec="black", pad=0.4)
        )

        # left child (earlier match)
        if node.left:
            plt.plot([x, x - dx], [y, y - 1], "k-")
            self._draw_top_down(node.left, x - dx, y - 1, dx / 2)

        # right child (earlier match)
        if node.right:
            plt.plot([x, x + dx], [y, y - 1], "k-")
            self._draw_top_down(node.right, x + dx, y - 1, dx / 2)

    # -------- public API --------
    def visualize(self, figsize=(18, 10), title="Tournament Match Tree (Top-Down)"):
        if self.root is None:
            raise ValueError("MatchTree has no root to visualize")

        plt.figure(figsize=figsize)
        self._draw_top_down(self.root, x=0, y=0, dx=1.6)
        plt.axis("off")
        plt.title(title)
        plt.show()

player_df = pd.read_csv("dataset/modified_espn_atp_rankings.csv")
player_df = player_df[player_df["Player"] != "Echargui M."]
current_player_list = player_df["Player"].tolist()
current_player_list = current_player_list[0: 128]
random.shuffle(current_player_list)

round_type = {'1st Round': 0, '2nd Round': 1, 'Quarterfinals': 2, 'Semifinals': 3, 
              'The Final': 4, '3rd Round': 5, '4th Round': 6, 'Round Robin': 7}
round_sequence = ["1st Round", "2nd Round", "3rd Round", "4th Round", "Quarterfinals", "Semifinals", "The Final"]

simulation_trees = []

instance = current_player_list
for round in round_sequence:
    winner_list = []
    for i in range(0, len(instance), 2):
        if round == "1st Round":
            match = GameMatchNode(instance[i], instance[i + 1], 3, 1, 2, round_type[round], "2025-11-23")
        else:
            match = GameMatchNode(instance[i].winner, instance[i + 1].winner, 3, 1, 2, round_type[round], 
                                  "2025-11-23", left = instance[i], right = instance[i + 1])
        match.deter_winner()
        winner_list.append(match)
    instance = winner_list
tree = MatchTree()
tree.root = instance[0]
tree.visualize()