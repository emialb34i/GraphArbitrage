import requests
import json
import os

API_KEY = os.environ.get('API_KEY')

def exchange_pairs():
    url = f"https://min-api.cryptocompare.com/data/v4/all/exchanges?{API_KEY}"
    response = requests.get(url)
    with open('exchange_pairs.json', 'w') as f:
        json.dump(response.json()["Data"]["exchanges"]["Binance"]["pairs"], f)

def connected_pairs():
    with open("exchange_pairs.json") as f:
        data = json.load(f)
    keys = list(data.keys())
    vals = [ list(data[k]["tsyms"]) for k in keys]
    return {k: v for k, v in zip(keys, vals) if len(v) > 3}

def spot_rates_snapshot():
    d = connected_pairs()
    snapshot = []
    for fsyms in list(d.keys()):
        tsyms = ','.join(d[fsyms])
        url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={fsyms}&tsyms={tsyms}&e=Binance&api_key={API_KEY}"
        res = requests.get(url).json()
        snapshot.append(res)
    with open("spot_rates_snapshot.json", "w") as f:
        json.dump(snapshot, f)

def create_adj_matrix():
    pass

if __name__ == '__main__':
    exchange_pairs()
    # spot_rates_snapshot()
