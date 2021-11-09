import json

with open("exchange_pairs.json") as f:
        data = json.load(f)

keys = list(data.keys())
vals = [ list(data[k]["tsyms"]) for k in keys]

d = {k: v for k, v in zip(keys, vals) if len(v) > 3}

print(d)