---
layout: post
title:  "Mark Zuckerberg personality insights"
date:   2018-03-21 19:47:54 +0000
---

Considering the attention drawn to data privacy after the recent Facebook and Cambridge Analytica fiasco, it seems relevant to explore some available tools for gathering insights on online publics. This article will experiment with IBM’s off the shelf personality insights tool to example the kinds of features that can be constructed from user data. It will use Mark Zuckerberg’s response to Cambridge Analytica’s apparent miss-use of Facebook data as a sample source.

## Introduction

The combination of modern psychology, big data and deep learning has opened possibilities for advertisers, political campaigns and others to personally target individuals on a massive scale. Research as such done by Michal Kosinski and others has continued to show a variety ways social media data can be used to predict personal attributes such as sexual orientation (Wang, Y. and Kosinski, M. 2018), age, gender and personality ([more citations?](http://www.michalkosinski.com/home/publications)). Though Cambridge Analytica’s impact on the 2016 U.S. election may be overstated, questions still arise to the effects of micro targeting can have on the functioning of democracies and to what extent have user’s consented to this subjection.


In this article IBM’s services are used as an example to demonstrate some generic models for creating insights from personal data. Mark Zuckerberg’s recent PR response posted publically on Facebook is given as example that will serve as the basis for the personality insights. Here it the sample text for your reference, if you would like to read it:


<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fzuck%2Fposts%2F10104712037900071&width=500" width="500" height="294" style="border:none;overflow:hidden;margin-bottom:24px;" scrolling="no" frameborder="0" allowTransparency="true"></iframe>

Beyond being a bit of fun, the example here aims to show how cheaply available insight tools are becoming whilst questioning there increasing use in society.

## Natural Language Understanding
Before going on to the results of the personality insights we can also quickly use IBM's [Natural Language Understanding](https://natural-language-understanding-demo.ng.bluemix.net/) API to get a brief outline of the document. Copy and pasting the Marks post into the demo site we get as follows:

<img src="{{ 'assets/imgs/mark-zuckerberg-personality-insights/toshare.png' | absolute_url }}"/>

As well as summarising the object of the text sample, we can see `I want to share` as key the subject/action of the message. This is describing the sematic roles of the document, what about the emotional content?

<img src="{{ 'assets/imgs/mark-zuckerberg-personality-insights/emotion.png' | absolute_url }}"/>

Interestingly the emotion is put forward as mixture of joy and sadness. Perhaps sadness because of the news, by optimistically joyful about prospects of your future with Facebook 💁.

## Personality Insights

Personality insights can arguably be used to gauge what kind of consumer you will be, the kind of products you will be more likely to buy and more increasingly what political messages may sway you. IBM’s [personality insights demo page](https://personality-insights-demo.ng.bluemix.net/) describes the service as follows:

> Gain insight into how and why people think, act, and feel the way they do. This service applies linguistic analytics and personality theory to infer attributes from a person's unstructured text.

Again, just copy and pasting Marks post into the demo yields a range of results, the first thing we are greeted by is high level summary shown below:

<img src="{{ 'assets/imgs/mark-zuckerberg-personality-insights/watson1.png' | absolute_url }}"/>

I always thought Mark was unlikely to be influenced by social media during product purchases but how did the application know that? Well according the what is described in the science of the services, specific personality profiles that are constructed suggest certain consumer behaviour. We can consider what this means a bit more with some of the other data the demo provides.


### Personality, Needs, Values

Diving into some of the data we see personality represented in three main categories:

__Big Five model__: This is one of the most widely studied personality models in clinical psychology. It describes a person in terms of _openness, conscientiousness, extraversion, agreeableness, and neuroticism_ - It is sometimes referred to as the OCEAN model. Here neuroticism has been renamed in the service as emotional range as it was thought more ‘generally applicable’ (IBM Cloud Docs, 2017).

__Needs__: _'The twelve categories of needs that are reported by the service are described in marketing literature as desires that a person hopes to fulfil when considering a product or service'_ (IBM Cloud Docs, 2017). (They are referring to: Kotler, P. and Armstrong, G. 2013. Principles of Marketing; Ford, K. 2005. Brands Laid Bare: Using Market Research for Evidence-Based Brand Management.)

__Values__: _'computes the five basic human values proposed by [Schwartz](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.220.3674&rep=rep1&type=pdf) and validated in more than twenty countries'_ (IBM Cloud Docs, 2017).

You can see the results of these fields below.

<img src="{{ 'assets/imgs/mark-zuckerberg-personality-insights/types.png' | absolute_url }}"/>

### A more detailed look at the Big Five

The service goes on to break-down the Big Five model into 10 features each making it 50 feature model. Because the more features the better right.

<img src="{{ 'assets/imgs/mark-zuckerberg-personality-insights/big5.png' | absolute_url }}"/>

If my graphs aren’t nice enough for you here’s a nice 👌'sun burst' visualisation of all the data shown above generated by the site.

<img src="{{ 'assets/imgs/mark-zuckerberg-personality-insights/sunburst.png' | absolute_url }}"/>

### Consumer Preferences

As stated previously inferences can be made about the kinds of choices individuals are likely to make based on specific personality traits. Using the features described above, models have been created by IBM to fit specific consumption preferences to specific personality types. Though not shown overtly on the demo page there is the option to download a JSON file with all the generic tests carried out. These can be listed as follows:

{% include mark.md %}

Some of these may seem silly, but in a real-world scenario you would create your own models to cater for your own specific needs. This part isn’t as cheap an endeavour and without existing data you would need to gather your own data for your needs.

## Conclusion

__How accurate is this?__

Short answer: In this example, not at all.

As the demo website states the sample is far too short to create an accurate analysis. However, say given a complete user profile the results are argued to become more effective. I found a few references to horoscopes in online discussions concerning the service ([Quora](https://www.quora.com/How-accurate-is-IBMs-Watson-Personality-Insights-application)).

Looking for other examples of this kind of service to get a comparison, the website created by Cambridge University [https://applymagicsauce.com/](https://applymagicsauce.com/) is probably the most similar available online. However, I didn’t try that one out in the end because it wanted access to my social media data.

With this kind of service the accuracy will always be hard to measure. Even though it is relying on numerical computations we are still receiving qualitative results. For example, agreeableness is much more a relative measure than a count of objects. Using tried and tested psychological frameworks means the service probably does have some merit however.


__Final thoughts__

Whether this is an accurate description of Mark’s personality or even the text is not the argument. This example was used to start to think about how tools trying to ascertain behavioural insights are integrating with society. The demo page emphasises that a represented sample be used. A person’s social media data tends to be thought of as a representative perhaps for its capacity for eclectic expression. This service and those like it will always be an assessment of a representation of a person not of them themselves. The question posed here is what constitutes a representative sample. The affordances of these services to those seeking insights depend on its accuracy but to those who are the subject of inquiry this is not always the case. For example, in the field of recruitment, services like that provided by [hirevue](https://www.hirevue.com/) use machine learning to gain insights on candidates scoring them via various metrics. Here, for the subject of inquiry accuracy is less important than a favourable outcome (i.e. getting the job). In this way, there is possibility for these tools to shape the behaviour of individuals. What happens when this becomes more widely used in society for decision making processes and is also further democratised? This could make for interesting future inquiry especially with regards to more civic matters.



### References

* Wang, Y. and Kosinski, M. 2018. Deep neural networks are more accurate than humans at detecting sexual orientation from facial images. _Journal of Personality and Social Psychology_. [Online]. [Accessed 22 March 2018]. __114__(2), pp.246-257. Available from: [https://psyarxiv.com/hv28a/](https://psyarxiv.com/hv28a/)
* IBM Cloud Docs, 2017. _The science behind the service_. [Online]. [Accessed 22 March 2018]. Available from: [https://console.bluemix.net/docs/services/personality-insights/science.html#science](https://console.bluemix.net/docs/services/personality-insights/science.html#science)
* IBM Watson Developer Cloud, 2017. _Personality Insights_. [Online]. [Accessed 22 March 2018]. Available from: [https://personality-insights-demo.ng.bluemix.net/](https://personality-insights-demo.ng.bluemix.net/)

### Other resources

* [IBM research reference list](https://console.bluemix.net/docs/services/personality-insights/references.html#fast2008)
* Costa, P., and McCrae. R. 2008. Revised NEO Personality Inventory (NEO-PI-R) and NEO Five-Factor Inventory (NEO-FFI) Manual. Odessa, FL: Psychological Assessment Resources (1992). Available from: [https://www.researchgate.net/publication/285086638_The_revised_NEO_personality_inventory_NEO-PI-R](https://www.researchgate.net/publication/285086638_The_revised_NEO_personality_inventory_NEO-PI-R)
* [Apply Magic Sauce personality insight app](https://applymagicsauce.com/)
* [Michal Kosinski - The End of Privacy, Keynote at CeBIT'17](https://www.youtube.com/watch?v=DYhAM34Hhzc)
* [http://www.michalkosinski.com/home/publications](http://www.michalkosinski.com/home/publications)
* [The Power of Big Data and Psychographics](https://youtu.be/n8Dd5aVXLCc)