import pandas as pd
from data import connected_pairs
import json
import networkx as nx
import numpy as np


def flatten(t):
    return [item for sublist in t for item in sublist]


with open("spot_rates_snapshot.json") as f:
    price = json.load(f)

data = connected_pairs()

keys = set(data.keys())
values = list(data.values())

all_pairs = list(keys.union(flatten(values)))

df = pd.DataFrame(columns=all_pairs, index=all_pairs)

for fsym in price:
    pairs = list(price[fsym].keys())
    for tsym in pairs:
        print(fsym, tsym, price[fsym][tsym])
        df.loc[fsym, tsym] = price[fsym][tsym]

df = df.fillna(0.0)
g = nx.DiGraph(df)

# df = nx.to_pandas_adjacency(g, dtype=int)
# print(df)