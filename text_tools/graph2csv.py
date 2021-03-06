'''
graph2csv.py

format list of nodes and edges generated by topic_graph.py into csv for use
with gephi software.
'''
from __future__ import print_function

import json
import csv

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", "--file", type=str, help="input filename", required=True)
parser.add_argument(
    "-o", "--out", type=str, help="output filename", required=True)
args = parser.parse_args()


with open(args.file) as fp:
    data = json.load(fp)
    links, nodes = data['links'], data['nodes']

glinks = []
for link in links:
    glinks.append({
        'source': nodes[link['source']]['name'],
        'target': nodes[link['target']]['name'],
        'weight': link['weight']})

with open(args.out, "w") as fp:
    fieldnames = list(glinks[0].keys())
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(glinks)

print("wrote to file: ", args.out)