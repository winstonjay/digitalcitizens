'''
topic_graph.py:

construct a graph in the form of links and nodes into json format
for use within javascript applications (d3.js in mind).

kinda a quick make do for now.

If the LDA model is taking too long for your liking, reduce the `max_iter` to
below 10 or reduce the `max_features`. It wil
'''
from __future__ import division
from __future__ import print_function

import numpy as np
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def topic_graph(data, max_features=5000, n_topics=5,
                n_samples=25, max_df=0.95, min_df=10,
                stop_words='english', ngram_range=(0, 1),
                max_iter=10, learning_offset=50.0, random_state=0):
    '''
    Construct a topic graph in the form of links and nodes into dictionary
    which is then easily convertable to json format. A topic graph is a
    bipartide graph where topics are connected by their corresponding terms.
    Topics are constructed by the sklearn's LatentDirichletAllocation model
    with overlapping terms forming the links between nodes. Optional args
    for the function correspond to optional args for both sklearns
    CountVectorizer and LatentDirichletAllocation models. These are not
    a complete list however.
    '''
    tf_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df,
                                    max_features=max_features,
                                    stop_words=stop_words,
                                    ngram_range=ngram_range)

    print("Fitting CountVectorizer...")
    tf_features = tf_vectorizer.fit_transform(data)
    tf_feature_names = tf_vectorizer.get_feature_names()

    print("Fitting LDA models with tf features, "
          "\nmax_iter=%d. number of topics=%d. n_samples=%d. features_shape=(%d, %d)..."
          % (max_iter, n_topics, n_samples, *tf_features.shape))
    print("This may take a while...")
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=max_iter,
                                    learning_method='online',
                                    learning_offset=learning_offset,
                                    random_state=random_state)

    # this will take a while. reduce max_iter to reduce this.
    t0 = time.time()
    lda.fit(tf_features)
    print("Model fitted in: {:.2f} secs".format(time.time() - t0))
    # print out the model created
    inspect_model(lda, tf_feature_names, n_samples)
    print("Fitting graph...")
    (nodes, links) = build_graph(lda, tf_feature_names, n_samples)
    print("done.")
    return {"nodes": nodes, "links": links}


def inspect_model(model, names, n_samples):
    for topic_idx, topic in enumerate(model.components_):
        print("#### topic:", topic_idx)
        for i in topic.argsort()[:-n_samples - 1:-1]:
            print("{}({:.2f})".format(names[i], topic[i]), end=", ")
        print()


def build_graph(model, names, n_samples):
    index = {}
    index_n = 0 # keep track of the node indexes.
    (nodes, links) = ([], [])
    for i, topic in enumerate(model.components_):
        topic_root = letters[i]
        nodes.append(Node(topic_root, True, 1))
        index[topic_root] = index_n
        index_n += 1
        for j in topic.argsort()[:-n_samples - 1:-1]:
            term = names[j]
            weight = topic[j]
            if term not in index:
                nodes.append(Node(term, False, weight))
                index[term] = index_n
                index_n += 1
            else:
                nodes[index[term]]['weight'] += weight
            link = Link(index[topic_root], index[term], weight, i)
            links.append(link)
    return (norm_scale(nodes), norm_scale(links))



# initialiser functions are used instead of classes as a short cut
# to create consitent representations of Nodes and Links.
def Node(name, root, weight):
    "pusedo Node struct constructor"
    return dict(name=name, root=root, weight=weight)

def Link(source, target, weight, group):
    "pusedo Link struct constructor"
    return dict(source=source,
                target=target,
                weight=weight,
                group=group)

def norm_scale(x, scale=True):
    "apply min max normalization"
    X = np.array([v['weight'] for v in x])
    X = 1 + np.log(X) # apply sub-linear scaling
    X = (X - X.min()) / (X.max() - X.min())
    for v, w in zip(x, X):
        v["weight"] = w
    return x

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


if __name__ == "__main__":
    # eg usage. Updata as you need.
    import json
    import pandas as pd

    df = pd.read_csv("../data/twitter/tweets_large_train", na_filter=False)

    graph = topic_graph(df.text)
    out = "../../gh-pages/_data/wordgraph.json"

    with open(out, "w") as f:
        json.dump(graph, f, indent=4, sort_keys=True)
    print("saved result to", out)
