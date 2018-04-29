---
layout: post
title:  "Twitter Spam and Ham"
date:   2018-04-01 18:00:43 +0100
---

Noting the wrangling needed to make Twitter data more useable and some make do solutions employed. This was supposed to be part of an upcoming post but has been separated to make the rest of the original article flow better.

{% assign static_path = "assets/imgs/twitter-spam-and-ham" | absolute_url %}

<img src="{{ static_path }}/tweep.jpg">

Though Twitter data generally is quite noisy and requires a lot of cleaning for analysis, what was collected for an upcoming post [Part 2: Twitter reactions to Facebooks ‘data leak’](#TODO) Initially was pretty much unusable.  This was due to massive amounts of spam targeting and also because the query terms were not rooted in any particular language. This post is mainly recorded for future reference when working with Twitter data.

### Spam tweets within the dataset
**The problem:**

Initial analysis of the tweets revealed that the tweets filtered for had been significantly targeted by spam and automated accounts. Without building a compressive spam filtering model this was most concretely revealed through examination of hashtag co-occurrences. A illustrative example of this case of spam could be 1000 tweets with exactly the hashtags:

```
#foo #tweet4tweet #bar #MontyPython
#fooBar #flyingCircus #CambridgeAnalytica
```

One set like this pertained over 2000 tweets with the same 6 hashtags an only 100 unique words between them. This was particularly disruptive to any computational analysis using any kind of frequency measure.

**Make do solution:**

Just applying some simple conditional logic we can decide whether a tweet is spam if has: either too many hashtags or if having above a certain threshold and whose set appears above a given limit within the tweet collection.  This can be expressed in Python code as follows:

```python
def is_spam(tags: tuple, ceil=10, floor=4, limit=40):
    return (True if len(tags) > ceil else
            True if len(tags) < floor
                 and collection_freq[tags] > limit else
            False)
```

The parameters given the algorithm ended up filtering `7%` of tweets.  [This paper](https://arxiv.org/pdf/1703.03107.pdf) studying bots on twitter in more detail estimates that around `9-15%` of all tweets currently come from spam accounts, so while almost in the same ball park this could have been more aggressive. Of 36925 tweets removed only 27 tag sets were regarded as spam.

Whether the parameters or method use was accurately effective is hard to say, it did render the dataset a lot more usable and seemingly less noisy. This problem of spam vs not spam is one of the classic examples given when teaching classification algorithms and merely using a something like a simple logistic regression model, more effective results could be made. However, due to the Twitters API terms of service permitting the sharing of datasets its quite hard to find labeled data to train a model on. There may be pre built solutions however, the problem may be very corpora specific however.


### Language Barriers

**The problem:**

Only being fluent in english and only knowing just enough French and Spanish to identify things like stop words (common low information words), tweets from other languages are not much use to me. Forgetting to collect the language information was something that caused more work here.

**Make do solution:**

Depending how aggressive an approach seemed relevant, several techniques seemed to work ok. An initial step was to remove certain character ranges. Pretty much everything out side of ascii was removed with the regular expression matching `[^\x00-\x7F]+`. This meant removing emoji and all sorts of things but they were not of interest here.

Another strategy was just adding more items to the stop word list and include words from different languages. The Python package [NLTK](https://www.nltk.org/), provides around 2,400 stop words for 11 languages, that wasn’t to time consuming to employ.



