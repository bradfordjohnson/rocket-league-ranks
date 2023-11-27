import pandas as pd
import json

with open("distributions.json") as json_file:
    data = json.load(json_file)

rank_distributions = pd.json_normalize(data, record_path=["values"], meta=["mode"])

rank_distributions.to_csv("rank_distributions.csv", index=False)
