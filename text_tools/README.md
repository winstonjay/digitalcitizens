
# Text tools

This folder contains scripts for pre-processing data and some implementations of some NLP algorithms. Some notable files:

* `rake.py` - Implements the RAKE (Rapid Automatic Keyword Extraction) algorithm.
* `chain.py` - Implements a basic Markov chain text generation algorithm.
* `spamfilter.py` - a Hashtag based twitter spam filter.
* `word2vec_basic.py` - Word to Vector algorithm, file taken from Tensorflow tutorial. Alterations made to suit my needs. Makes nice t-SNE graph from the input data.
* `topic_graph.py` - Generate a bipartide graph of topics and topic words that is easily serialized into json for use in javascript application. Topic graph is generated from Latent Dirichlet Allocation model where overlapping terms betwen topics form the connecting nodes.
