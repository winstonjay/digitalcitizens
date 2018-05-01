---
layout: post
title:  "Data, politics and democracy part 2: Twitter reactions to Facebooks ‘data leak’"
date:   2018-04-12 23:22:45 +0100
---
Using data collected whilst the Facebook/Cambridge Analytica story was first gaining momentum, this post looks at the responses made to it via Twitter. Experimenting word embedding’s and other computational methods, it aims to map key dimensions that highlight the contextual relationships between different sentiments across the dataset.

{% assign static_path = "assets/imgs/data-politics-and-democracy-part-2" | absolute_url %}

<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=TeX-MML-AM_CHTML' async></script>

## Introduction

This section of the series can be outlined as follows. First a brief rational is given on why Twitter is being used as a site of research rather than Facebook. Second Analytical methods will be introduced. These include the computation of word embedding’s and a devised simpler variation seeking to find shared contexts between terms within tweets. Thirdly findings will be discussed and finally a brief conclusion will be made.

### Twitter over Facebook

It is probably fitting to answer why Twitter is being used to explore an issue most concerning Facebook users. One answer is simply, because it is easier and cheaper. Another is arguably that Twitter is far more clearly configured for the public expression of sentiment.

**Collection cost**

It is cheaper to collect the kind of public response data in mind on Twitter rather than Facebook due to the design of their data collection services. For aggregating posts real-time, Twitter’s has its [Streaming API](https://developer.twitter.com/en/docs/tweets/filter-realtime/overview) which is open for anyone to use. The closest thing Facebook has to this is its [Public Feed API]( https://developers.facebook.com/docs/public_feed/). Access to this is restricted to a limited set of pre-approved ‘media publishers’. To access Facebook user data at scale, you must either pay, have special institutional privileges, be providing a widely-used service or pretty much trick users into sharing it with you.

**What’s being shared**

Regarding the character of the content created within each site, there are specific design aspects to each that could have a formative effect on what is shared. This presents differences in the usefulness of each for this investigation. On Facebook, a user principally addresses their ‘friends’, on Twitter it’s their ‘followers’, this is reflected in the default post visibility settings. Facebook asks ‘what’s on your mind?’, Twitter asks ‘what’s happening?’. Ultimately, the difference in what each site purveys as it purpose is; Facebook is about connecting people, and Twitter is about connecting people to current affairs. For this and the reasons discussed above, though not perfect, Twitter seems it’s a more appropriate tool to learn about public interaction with current affairs.

**Short-comings**

Though it may provide means for investigating sentiment on an international scale, public posts made on Twitter are undoubtedly not a reflective sample of all public opinion, even of the opinions of all Twitter users. Though it provides large amounts of data, its quality is often hard to determine. As we will see in this section, it can be especially messy at times. These themes and other critical engagements are discussed in more detail in a previous post ([Notes on Digital Methods](#TODO)).


## Approach
Approximately 500,000 tweets were collected using Twitters [streaming API ](https://developer.twitter.com/en/docs/tweets/filter-realtime/overview) between the 20th and the 23rd of March 2018, filtering for the query terms `Facebook` and `Cambridge Anaylitica`. This was just after the Guardian’s [initial story](https://www.theguardian.com/news/2018/mar/17/data-war-whistleblower-christopher-wylie-faceook-nix-bannon-trump?CMP=twt_gu) was released and was gaining traction across social and broadcast media. Simple measures such as hashtag frequency were used in combination denser word representations, such as word embedding’s. These were used to form a fast but distant reading of the dataset. This experimentation provides a contextual overview of the response to help identify specific attributes for moving forward.

---

### Word embedding’s


Vector representations of words, or [vector space models]( https://en.wikipedia.org/wiki/Vector_space_model), aim to map the semantic similarity of words in continuous vector space. This can This has advantages over the more traditional bag of words model as it provides denser representations of terms. Instead of treating individual terms as unique identifiers, we can embed contextual information within them. For example, the similarities cats and kittens do and don’t have.

<img src="{{ static_path }}/dataspace.jpg"/>

This idea depends on the [distributional hypothesis]( https://en.wikipedia.org/wiki/Distributional_semantics#Distributional_Hypothesis), which implies that semantically similar words occur in similar contexts. As J.R. Firth summarises *’you shall know word by the company it keeps’*. Though the definition of what constitutes a context can vary here we will just assume context is created by a window of neighbouring words.

**Count based methods**

For my own notes, an illustrative example is given (Example is slight variation on that provided in Grefenstette, E. 2017).

$$
\begin{align}
& \text{... the cute kitten purred ...}\\
& \text{... the old furry cat meowed and purred ...}\\
& \text{... the small furry kitten meowed ...}\\
& \text{... an loud furry old dog barked ...}\\
\end{align}
$$

Say we are just interested in words `kitten`, `cat`, and `dog`. If we set our context window to 2 words either side of our target words. With stop words removed we can create a set of witnessed context words for each.

$$
\begin{align}
& \textbf{kitten}: & & cute, purred, small, furry, meowed\\
& \textbf{cat}   : & & old, furry, purred\\
& \textbf{dog}   : & & loud, furry, old, barked \\
\end{align}
$$

After this small example our complete set of context vocabulary would be: `{cute, purred, softly, small, meowed, furry, old}`. Using this generated vocabulary, one way we can create a vector representation is as follows:

$$
\begin{align}
\text{kitten}&=\left[ \begin{array} &1& 1& 1& 1& 1& 0& 0& 0 \end{array} \right]\\
\text{cat}   &=\left[ \begin{array} &0& 1& 0& 1& 1& 1& 0& 0 \end{array} \right]\\
\text{dog}   &=\left[ \begin{array} &0& 0& 1& 0& 0& 1& 1& 1 \end{array} \right]\\
\end{align}
$$

This indexes each of the word in the context vocabulary with either a 0 or a 1 depending if the context word appears within the same context as our target words. This is useful as we can now compute the similarity between each word, for instance with cosine similarity.


$$
cosine(\pmb u, \pmb v) = \frac {\pmb u \cdot \pmb v}{||\pmb u|| \cdot ||\pmb v||}
$$

The numerator of the equation here is the [dot product]( https://en.wikipedia.org/wiki/Dot_product) of the two vectors and the denominator is the product of the 2 [Euclidian norms]( https://en.wikipedia.org/wiki/Norm_(mathematics)#Euclidean_norm). Actually computing this, as is expected from this completely constructed example `kitten` is most like `cat`. Wow how did that happen? Also, the fact that both `cat` and `dog` have `old` in their context, `dog` is more like `cat` than `kitten`.



$$
\begin{align}
cosine(\text{kitten}, \text{dog}) & \approx 0.33\\
cosine(\text{cat}, \text{dog}) & \approx 0.25\\
cosine(\text{cat}, \text{kitten}) & \approx 0.68\\
\end{align}
$$

**Neural Embedding’s**

Beyond count based methods neural embedding’s have also been widely employed to predict vector representations. It’s the same basic idea just with more linear algebra and it sounds cooler. Two of the main modelling strategies here, are the Continuous Bag-of-words model (CBOW) and the Skip-gram model. They function in pretty much opposite ways. Here is an illustration comparing both:

<img src="{{ static_path }}/skipgram.jpg"/>
<small>Image from: (Mikolov, T. Chen, K. et al. 2013) [https://arxiv.org/abs/1301.3781]( https://arxiv.org/abs/1301.3781)</small>

The CBOW model tries to predict the target word from a given set of context words and the Skip-gram model tries to predict the context words given a target word. In this post the Skip-gram model is used, implemented with the machine learning library Tensorflow. This was done with reference to their demonstration [word2vec_basic.py]( https://github.com/tensorflow/tensorflow/blob/r1.7/tensorflow/examples/tutorials/word2vec/word2vec_basic.py). Alterations to the original file have been made to pre-process the data differently and carry out some additional steps.

**Visualising vector representations**

Word vector representations produce high dimensional representations. To make sense of the representations better we can project them in to lower dimensional space. This will be done here using t-distributed stochastic neighbour embedding (t-SNE) implemented using the Python package Scikit-Learn.



### Co-occurrences

In this post the Skip-gram model is used, implemented with the machine learning library Tensorflow. This was done with reference to their demonstration [word2vec_basic.py]( https://github.com/tensorflow/tensorflow/blob/r1.7/tensorflow/examples/tutorials/word2vec/word2vec_basic.py). Alterations to the original file have been made to pre-process the data differently and carry out some additional steps.


Another more simplified count based model was also used to explored the contextual relationships between the data. Instead of using an arbitrary window size to determine whether terms appeared in the same context, the context window is instead the set to the whole tweet. The typical number of words per tweet with stop words removed is only around `X` (look up), therefore the context window shouldn’t be too large. Instead of making predictions about the similarity of words here the aim is to just to measure the contextual links between terms. This will be performed on a select vocabulary of interest instead of the whole dataset.
The methods for investigating the data here are experimental in a way that is trying to learn about methodological approaches and the data simultaneously.

### Noise within the data
As discussed in a previous post the dataset collected here was especially noisy. As a reminder, this came in the form of spam targeting the trending topic but also the fact that Tweets from a wide variety of languages. The topic followed was markedly an internationally discussed issue and it didn’t help that the query terms were organisation names instead of words belonging to the English language.

## Findings

### Hashtags
Looking at hashtag frequencies, we can see that `deleteFacebook` was the most popular – something that was also widely reported by news organisations. Whilst filtering spam it was noted many tweets contained nothing but this repeatedly. Some of these Tweets looked like they come from automated accounts some, others more natural. This did pose some questions of trend manipulation, but after counting the document frequencies and not repeats within tweets there was not much change in the results. Below the top ten tags can be seen with the query terms (‘Facebook’, ‘CambridgeAnalytica’) filtered from the collection. Taking this approach there doesn’t seem to be anything too overt to help that helps explore the topic in from any new directions.

<img src="{{ static_path }}/tags.png"/>

### Co-occurrences

<img src="{{ static_path }}/cooccurances.png"/>


### Word embedding’s

Running the Tensorflow model described previously for 10,000 iterations it finished with an average loss of around 4% in predicting contexts of given terms within the training data. Evaluation of how well the model performs in practice is obviously harder to determine. The size and quality of the data put into the model is obviously not going to give a good representation of the English language but it may have the potential to map corpora specific terms and Ideas. Below is a T-SNE visualisation of the word embedding’s created.


<img class="big-img" src="{{ static_path }}/tweets4_tsne.png">

**Annotating the Space**

As mentioned before T-SNE visualisations can be another cause for confusion, tending themselves to be easily miss-read, hopefully that won’t be the case here lol. Running the visualisation program several times, the intuitive understanding is, that while global positioning within the graph tends to vary, local relevant terms produce more repeatable results. For example, the small group of un-filtered French stop words `vous, mias, pour, dans` near each other. Logically French words are not likely to appear in the same context as English ones, so that seems correct. Common bigrams such as `fake news, social platforms, public security` seem to have clustered.


<img src="{{ static_path }}/annotated.jpg"/>

### References

* Grefenstette, E. 2017. *Lecture 2a- Word Level Semantics*. Available from: [lectures/Lecture 2a- Word Level Semantics.pdf at master · oxford-cs-deepnlp-2017/lectures · GitHub](https://github.com/oxford-cs-deepnlp-2017/lectures/blob/master/Lecture%202a-%20Word%20Level%20Semantics.pdf)
* Jurafsky, D. and James, M. 2009. *Speech and Language Processing*. Second Ed. London, UK: Pearson Education Ltd ([Third Ed is available here online]( https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf))
* Maaten, Laurens van der, and Geoffrey Hinton. 2009. Visualizing data using t-SNE. *Journal of Machine Learning Research*. pp.2579-2605. Available from:[http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf)
* Mikolov, T. Chen, K. et al. 2013. *Efficient Estimation of Word Representations in Vector Space*. Availible from: https://arxiv.org/abs/1301.3781
* [Vector Representations of Words  -  TensorFlow](https://www.tensorflow.org/tutorials/word2vec)
* [Word2Vec Tutorial - The Skip-Gram Model · Chris McCormick](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/)



### Additional resources:
* [Firth, John R. "A synopsis of linguistic theory, 1930-1955." (1957): 1-32.](http://annabellelukin.edublogs.org/files/2013/08/Firth-JR-1962-A-Synopsis-of-Linguistic-Theory-wfihi5.pdf)
* [Mikolov, Tomas, et al. "Distributed representations of words and phrases and their compositionality." Advances in neural information processing systems. 2013.](http://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)
* [LDA2vec: Word Embeddings in Topic Models (article) - DataCamp](https://www.datacamp.com/community/tutorials/lda2vec-topic-model)
* [GitHub - MaxwellRebo/awesome-2vec: Curated list of 2vec-type embedding models](https://github.com/MaxwellRebo/awesome-2vec)
* [Anything2Vec, or How Word2Vec Co nquered NLP](http://nlp.town/blog/anything2vec/)


---

#### Read Next: [Data, politics and democracy part 3]({{ site.baseurl }}{% post_url 2018-04-12-data-politics-and-democracy-part-3 %})
