import pandas as pd
import json
import re

with open('distributions.json') as json_file:
    data = json.load(json_file)

rank_distributions = pd.json_normalize(data, record_path=['values'], meta=['mode'])

rank_distributions['min'] = rank_distributions['division_1'].str.split(' - ').str[0]
rank_distributions['max'] = rank_distributions['division_4'].str.split(' - ').str[1]


rank_distributions = rank_distributions.sort_values(['mode', 'min'], ascending=[True, True])
rank_distributions['order'] = rank_distributions.groupby('mode').cumcount()+1

print(rank_distributions)
rank_distributions.to_csv('rank_distributions.csv', index=False)
