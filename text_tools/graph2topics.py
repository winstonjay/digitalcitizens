'''
graph2topics.py:

transfer topic graph back into a list of topics. this is kind of stupid but
should be easier that the alternatives.
'''
from __future__ import print_function

import json
import collections
import random

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", "--file", type=str, help="input filename", required=True)
parser.add_argument(
    "-o", "--out", type=str, help="output filename", required=True)
args = parser.parse_args()

def shuffled(data):
    data_copy = data[:]
    random.shuffle(data_copy)
    return data_copy

with open(args.file) as fp:
    data = json.load(fp)
    links, nodes = data['links'], data['nodes']

groups = "ABCDE"

topics = collections.defaultdict(list)

for link in links:
    node_index  = link['target']
    node_weight = link['weight']
    group = link['group']
    topics[group].append({'name': nodes[node_index]['name'],
                          'weight': node_weight})

buffer = ["<div class='topics'>"]

item_template = "\t\t<span style='font-size:{}px; opacity:{}'>{}</span>"
# basic check to see this went as planned.
for k, vals in topics.items():
    assert len(vals) == 25, "wrong size group got=%d" % len(vals)
    buffer.append("\t<p>")
    for v in shuffled(vals):
        opacity = min(1, 0.5 + v['weight'])
        font_size = round(8 + (v['weight'] * 24), 1)
        buffer.append(item_template.format(font_size, opacity, v['name']))
    buffer.append('\t</p>')
buffer.append("</div>")


with open(args.out, "w") as fp:
    fp.write('\n'.join(buffer))

print("wrote to file:", args.out)