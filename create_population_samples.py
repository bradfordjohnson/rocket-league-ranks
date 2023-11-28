import pandas as pd
import json
import re
import random

with open("distributions.json") as json_file:
    data = json.load(json_file)

rank_distributions = pd.json_normalize(data, record_path=["values"], meta=["mode"])

rank_distributions["min"] = rank_distributions["division_1"].str.split(" - ").str[0]
rank_distributions["max"] = rank_distributions["division_4"].str.split(" - ").str[1]

rank_distributions["players"] = pd.to_numeric(
    rank_distributions["players"], errors="coerce"
)
rank_distributions["min"] = pd.to_numeric(rank_distributions["min"], errors="coerce")
rank_distributions["max"] = pd.to_numeric(rank_distributions["max"], errors="coerce")

rank_distributions["max"] = rank_distributions["max"].fillna(1800)

def generate_random_mmr(min_mmr, max_mmr):
    return random.randint(int(min_mmr), int(max_mmr))


player_records = []

for _, row in rank_distributions.iterrows():
    rank = row["rank"]
    mode = row["mode"]
    min_mmr = row["min"]
    max_mmr = row["max"]
    num_players = row["players"]

    mmr_values = [generate_random_mmr(min_mmr, max_mmr) for _ in range(num_players)]

    player_records.extend(
        [{"rank": rank, "mode": mode, "mmr": mmr} for mmr in mmr_values]
    )

result_df = pd.DataFrame(player_records)

rank_order = {
    "Supersonic Legend": 1,
    "Grand Champion III": 2,
    "Grand Champion II": 3,
    "Grand Champion I": 4,
    "Champion III": 5,
    "Champion II": 6,
    "Champion I": 7,
    "Diamond III": 8,
    "Diamond II": 9,
    "Diamond I": 10,
    "Platinum III": 11,
    "Platinum II": 12,
    "Platinum I": 13,
    "Gold III": 14,
    "Gold II": 15,
    "Gold I": 16,
    "Silver III": 17,
    "Silver II": 18,
    "Silver I": 19,
    "Bronze III": 20,
    "Bronze II": 21,
    "Bronze I": 22,
}

result_df["rank_order"] = result_df["rank"].map(rank_order)

result_df.to_json("sample_population.json", orient="records")
