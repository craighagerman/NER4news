# Background Information


## On Named Entity Recognition Classes

NER systems and use cases recognize different number of entities. These are generally one of 3 classes of model:

- 3-class: organization, person and location only
- 4-class: organization, person, location and miscellaneous
- 7-class: organization, person, location, date, money, time, percentage



## NER Approaches

NER systems can be implemented in one of four ways


1. Dictionary approach

- Use a key-value dictionary to define entities
- Simply look up each token in a text to see if it is in the dictionary
- n.b. This is a very simplistic approach. Only useful for limited use cases.


2. Rule Based approaches

- Define a set of rules (e.g. using Regular Expressions) for patterns
    - e.g. a token following "Dr/Mr/Ms/Mrs" is name 
- Such rules are usually manually created/curated
- This approach is sufficient for some use cases and can be extended by adding more and more rules. Internally Bloomberg News uses a very elaborate legacy rules based system to annotate news articles with "tags".


3. Classical Machine Learning approaches

- Use a supervised learning classifier (e.g Naive Bayes classifier)
- Train a model on labeled training data to predict the class for each entity
- n.b. this requires LABELED data (i.e. training data with entity classes labeled must be available)
- n.b. this approach likely requires exploratory data analysis and feature exploration to (1) identify good/relevant features and (2) an optimal approach to representing those features
    - e.g. (1) perhaps we hypothesis that "capitalization of initial letter" of a word is a useful feature. We must then also determine how to represent that feature in the input data for our model
    - e.g. (2) it is likely we want to do some morphological analysis as a preprocess step and do either stemming or lemmatization to normalize tokens.
- I include in "classical ML approaches" statistical methods such as using Hidden Markov Models (HMMs).
- This approach is more robust and generalizable than a rule-based approach but requires (1) a large corpus of (2) labeled data and (3) semi-manual feature exploration. All SoTA NER approaches before mid 2010's used this kind of approach.


4. Deep Learning ML approaches

- At a high level, this is identical to classical approaches - a supervised classifier is trained on labeled data to identify and predict entity classes.
- The difference viz. classical approaches are (1) DL approaches learn complex feature representations without manual feature exploration and (2) vast quantities of training data are needed


## Issues in NER

**Generalization**
- A ML model should generalize to new, unseen data. If new data is very different from that used for training the model may be unable to generalize sufficiently well. This can also be the case if/when there is a shift in data patterns over time. (e.g. city names become popular as given names.)

**Abiguity**
- Does "Apple" refer to the fruit or a company? Is Paris a name (Paris Hilton) or a location (Paris, France) or organization (Paris 2024)?

**Context dependency**
- Goes along with the above. Often a term on it's own is insufficient to determine the entity class and the context must be considered.




