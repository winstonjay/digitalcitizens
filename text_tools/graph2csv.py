from __future__ import division
from __future__ import print_function

import json
import csv
# transfer topic graph back into a list of topics. this is kind of stupid but
# should be easier that the alternatives.

data_path = "../../gh-pages/_data/wordgraph.json"
out_path = "../data/gelphi0.csv"


with open(data_path) as fp:
    data = json.load(fp)
    links, nodes = data['links'], data['nodes']

glinks = []
for link in links:
    glinks.append({
        'source': nodes[link['source']]['name'],
        'target': nodes[link['target']]['name'],
        'weight': link['weight']})

with open(out_path, "w") as fp:
    fieldnames = list(glinks[0].keys())
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(glinks)

print("wrote to file: ", out_path)