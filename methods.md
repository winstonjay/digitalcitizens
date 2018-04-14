---
layout: page
title: Methods
permalink: /methods/
---

This page will serve as a repository of computational methods of collecting, sampling and representing social data in digital environments.

The examples that follow come from a variety of sources and contextual backgrounds. Some are designed for use within the context of research and some do not have their origin in research but propose opportunities for repurposing.

---

## Exploring YouTube recommendations

Guillaume Chaslot (AlgoTransparency) - [https://github.com/pnbt/youtube-explore](https://github.com/pnbt/youtube-explore)

Uses Youtube recommendations to explore how likely particular content is to be seen. It was designed to answer the question:

> Where does YouTube's recommendation algorithm bring the user if he follows the recommendations?

**Description in [source code](https://github.com/pnbt/youtube-explore/blob/master/follow-youtube-recommendations.py):**

```
This scripts starts from a search query on YouTube and:
	1. gets the N first search results
	2. follows the first M recommendations
	3. repeats step (2) P times
	4. stores the results in a JSON file
```

After this, the idea is to count the number of recommendations of each video.

Due to the personalisation of Youtube questions arise in how this could reflect the content trajectories of different accounts. In the use case given by the author, it uses an account with no viewing history. As soon as a search is made is that account then compromised?

The method provided is used by the  [AlgoTransparency](https://algotransparency.org/) project.

---

## Find Birds

Andrej Karpathy  -  [https://github.com/karpathy/find-birds](https://github.com/karpathy/find-birds)

Script was designed to find who the people you follow are following and therefore advise on who you should follow in the future.

In the context of social research the collection process is essentially a implementation of snowball sampling using Twitters API.

**Interpretation of algorithm:**

```
With Twitter's API...

for each user that you follow:
	1. get all profiles of users they follow.
	2. commit profiles to file/database.

Count occurrences of accounts.
```

The implementation only goes one level deep as the author states that due to the API rate limiting this will take something like a couple days.

---

## IssueCrawler
Govcom.org Foundation - [IssueCrawler](https://www.issuecrawler.net/)

IssueCrawler is a _“web network location and visualisation software”_. Concretely it is a web crawler suite designed to help social researchers study networks.

The idea is you give it a list of urls as starting points to crawl from, it does this for you and then provides means to visualise the results. The tool crawls websites in three main ways, these are (quoting from their instructions website):

* “**Snowball analysis** crawls sites and retains pages receiving at least one link from the seeds.”
* “**Inter-actor analysis** crawls the seed URLs and retains inter-linking between the seeds. “
* “**Co-link analysis** crawls the seed URLs and retains the pages that receive at least two links from the seeds.”

There is a mass of instructions for use and use cases which I haven’t explored fully. If interested it would be better to visit their site: [GOVCOM.ORG](http://govcom.org/Issuecrawler_instructions.html). I have mainly posted this here for future reference.

---

## Topic Extraction

Topic Extraction or topic generation provides a way to automatically generate topics from text data. There are a number of ways of implementing this.

#### Latent Dirichlet Allocation (LDA)

Latent Dirichlet Allocation (LDA) is generative probabilistic model well suited for textual data summarisation (Blei, D.M., Ng, A.Y. and Jordan, M.I. 2003. p.993). What this essentially does is iteratively generate random groups of words from the dataset testing the probability of co-occurrences of terms, optimising for a specific number of iterations trying to increase the probabilities of terms existing within each set. In the process this generates what resembles real topics in the data (2003).

**Rough Pseudo code:**

```
1. Randomly assign each word in each document to one of K topics
2. for each document as d:
  (assume all topic assignments except current are correct.)
  for each word as w:
    for each topic as t:
      a := P(topic t | document d)),
        (the proportion of words in document
         d that are currently assigned to topic t)
      b := P(word w | topic t)
        (the proportion of assignments to topic t
         over all documents that come from this word w)
      assign w to a new topic based on a * b
3. Repeat step 2 until halt condition is met.
```

(maybe some mistakes and missing details.) Halt condition can be either a max number of iterations or a given loss threshold.

Python programming Implementation is made easily available through:
[sklearn.decomposition.LatentDirichletAllocation — scikit-learn 0.19.1 documentation](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html)

**Ref / more learning resources for me**:

* [Blei, D.M., Ng, A.Y. and Jordan, M.I. 2003. Latent Dirichlet Allocation. Journal of Machine Learning Research. 3(1). pp.993-1022.](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
* [Introduction to Latent Dirichlet Allocation](http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/)
* [GitHub - blei-lab/onlineldavb: Online variational Bayes for latent Dirichlet allocation (LDA)](https://github.com/blei-lab/onlineldavb)

---

fin.

## Other links

These sites have their own list of methods:

* [Digital Methods Initiative](https://wiki.digitalmethods.net/Dmi/ToolDatabase)