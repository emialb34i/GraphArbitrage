import requests
import json
import os
import pandas as pd
from tqdm import tqdm

API_KEY = os.environ.get('API_KEY')


def flatten(t):
    return [item for sublist in t for item in sublist]


def exchange_pairs():
    # returns pairs tradable on binance
    url = f"https://min-api.cryptocompare.com/data/v4/all/exchanges?{API_KEY}"
    response = requests.get(url)
    with open('data/exchange_pairs.json', 'w') as f:
        json.dump(response.json()["Data"]["exchanges"]["Binance"]["pairs"], f)


def connected_pairs():
    # process raw json file to return dict of tradable pairs on Binance
    with open("data/exchange_pairs.json") as f:
        data = json.load(f)
    keys = list(data.keys())
    vals = [list(data[k]["tsyms"]) for k in keys]
    return {k: v for k, v in zip(keys, vals)}


def spot_rates_snapshot():
    # fetches the exchange rates for all pairs tradable on Binance
    d = connected_pairs()
    snapshot = {}
    for fsyms in tqdm(list(d.keys())):
        tsyms = ','.join(d[fsyms])
        url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={fsyms}&tsyms={tsyms}&e=Binance&api_key={API_KEY}"
        res = requests.get(url).json()
        snapshot.update(res)
    with open("data/spot_rates_snapshot.json", "w") as f:
        json.dump(snapshot, f)


def create_adj_matrix():
    # creates an adjcecency matrix by turning the spot rates 
    # snapshot into a dataframe and saves it as a csv
    data = connected_pairs()

    with open("data/spot_rates_snapshot.json") as f:
        price = json.load(f)

    keys = set(data.keys())
    values = list(data.values())
    all_pairs = list(keys.union(flatten(values)))

    df = pd.DataFrame(columns=all_pairs, index=all_pairs)

    for fsym in price:
        pairs = list(price[fsym].keys())
        for tsym in pairs:
            df.loc[fsym, tsym] = price[fsym][tsym]

    # df = df.dropna(how='all', axis=1)
    # df = df.dropna(how='all', axis=0)
    # TODO add fiat currencies exchange rates 
    df = df.fillna(0.0)

    df.to_csv("data/snapshot.csv")

    return df
