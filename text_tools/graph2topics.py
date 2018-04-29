from __future__ import division
from __future__ import print_function

import json
import collections
import random
# transfer topic graph back into a list of topics. this is kind of stupid but
# should be easier that the alternatives.

data_path = "../../gh-pages/_data/wordgraph.json"
out_path = "../../gh-pages/_includes/topictable.html"


def shuffled(data):
    data_copy = data[:]
    random.shuffle(data_copy)
    return data_copy

with open(data_path) as fp:
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


with open(out_path, "w") as fp:
    fp.write('\n'.join(buffer))

print("wrote to file:", out_path)