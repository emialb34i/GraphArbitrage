import requests
import json
import time

API_KEY = "b4a25ed0b5226baed12a4087c91f31b21300f861a2accda388769cd527405cd3"

def exchange_pairs():
    url = f"https://min-api.cryptocompare.com/data/v4/all/exchanges?{API_KEY}"
    response = requests.get(url)
    with open('exchange_pairs.json', 'w') as f:
        json.dump(response.json(), f)

def connected_pairs():
    with open("exchange_pairs.json") as f:
        data = json.load(f)
    keys = list(data.keys())
    vals = [ list(data[k]["tsyms"]) for k in keys]
    return {k: v for k, v in zip(keys, vals) if len(v) > 3}

def spot_rates_snapshot():
    url = f"https://min-api.cryptocompare.com/data/v2/pair/mapping/exchange?e=Binance&api_key={API_KEY}"
    response = requests.get(url)
    with open('spot_rates_snapshot.json', 'w') as f:
        json.dump(response.json(), f)

    

if __name__ == '__main__':
    exchange_pairs()
    spot_rates_snapshot()
