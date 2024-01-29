# NER4news
Named Entity Recognition for news articles


--------------------

## Getting Started

### Prerequisites

- terminal
- pyenv and virtualenv must be installed

References
- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)


### Install a python version into pyenv

```
$ pyenv install  3.11.6
```

### Create a new virtualenv

```
$ pyenv virtualenv 3.11.6 ner
```

### Activate the virtualenv

```
$ pyenv activate ner
```

### Install python dependencies

```
$ cd NER4news
$ pip install -r requirements.txt
```

### Install SpaCy Transformer NER model

```
python -m spacy download en_core_web_trf
```


### Clean up

n.b. When you are done with the virtualenv it can be deactivated

```
$ pyenv deactivate
```


--------------------


## Extract NER entities and enrich articles

n.b. This will take a VERY long time to run (about an hour)

```
$ python ner4news/pipeline.py data/raw/cnn_data.zip
```

Alternately I've included an option to process just the first N rows of data instead. To process the first 10 rows run this instead

```
$ python ner4news/pipeline.py data/raw/cnn_data.zip 10
```

Which should only take a couple of minutes to run




--------------------

## Repo overview

The repo contains the following directories

**data**
- raw: to hold the raw input data (i.e. cnn_data)
- external: for any external datasets
- interim: for all interim data we want to persist, including model evaluation from Jupyter notebook experiments
- processed: for the processed articles enriched with entities

**docs**
- contains some extra documentation beyond this Readme

**ner4news**
- the source code directory

**notebooks**
- jupyter notebooks for exploration & experiments
- n.b. I experimented with 4 NER models (Spacy, Bert, Flair, Stanford) and computed evaluation metrics on each using the same CONLL2003 dataset
- n.b. I ran each of these on a GPU cloud server (Vast.ai). They are quite memory and computationally expensive. (e.g. models in the 400MG-1GB size, and taking a very long time to run on a local CPU machine.) For this reason the dependences of each of those are NOT included in the requirements file but will be automatically downloaded when running each notebook.
- n.b. each of the notebooks has been saved as both .html and .pdf filetypes for read-only viewing


## ner4news source code directory

`pipeline.py`
- the main entry point
- defines and runs a simple pipeline to perform preprocessing, NER extraction and persisting data

`preprocess.py`
- Contains a class for preprocessing input data

`ner.py``
- Contains a class for enriching an Article object with NER entities (using Spacy)


`obj`
- module for holding dataclass objects (internal data structures)

`util`
- helper functions






--------------------

## The Approach

There are 3 general approaches to doing NER for production/industry use

1. Use an off-the-shelf framework with a good built-in NER model (e.g. Spacy)
2. Use a general purpose language model with an NER tagger (e.g. Bert_based)
3. Fine tune a language model in #2

see this document for more info on NER approaches
- docs/Background_Info.md

I chose approach #1 above using Spacy. 
- It's better to get off the ground faster by using a well-known, stable framework with excellent all around NLP performance. 
- It is also the only model (of the 4 I experimented with) which handled MORE than 4 NER class labels. (The CONLL2003 dataset that many NER models are trained on contains only PERSON, ORGANIZATION, LOCATION and MISCELLANEOUS). Since there are more entity classes mentioned in the requirements this makes Spacy a good choice. 




## Data Preprocessing

The cnn_data.zip data contains a list of JSON objects. I conducted some quick EDA (Exploratory Data Analysis). 

see:
-[EDA](docs/EDA.md)

The data preprocessing does the following
- uncompress cnn_data.zip
- deserialize the raw JSON data into an internal data structure (CNNArticle)
- parse the raw_content for clean text
- enrich the Aricle object with `highlights` and `body` texts

n.b. No other data wrangling or preprocessing is needed. The NER models I used include robust tokenization and do not require more than clean sentences as input.



## Model Evaluation

The `cnn_data.zip` file is not labeled data. Therefore, it is not possible to compute any evaluation metrics on this data as is. 

> [!Note] Computing Precision, Recall, F1, Accuracy or other metrics requires there be ground truth data. i.e. "labels". For and NER task that means we need to have a test dataset containing both texts and ground truth labels about the entity classes in those texts.

n.b. I consider this a good "real world" task since (1) most datasets in the wild aren't labeled and (2) managers do often ask about evaluation metrics. So the question is really "how can we evaluate and approach when we don't have labeled data"

There are two solutions

1. manually label data (this is usually unfeasible in enterprise)
2. use a different labeled dataset (assumed to be similar)

For #2 the best choice is probably the CONLL2003 dataset. This has been used for 20 years for NER (and other) computational linguistics papers. The data is derived from newspaper articles so can be assumed to be a fair proxy for the CNN data. The other choice would be Ontonotes. But this corpus contains various genres and thus wouldn't be as good an analogue for CNN data. One caveat about CONLL2003 is that it only uses 4 NER classes. 

I ran experiments (in jupyter notebooks in the `notebooks` directory) using 4 models. The evaluation metrics from each are in the `data/interim` directory as `evaluation_results_*.json` files. n.b. The spacy file is in a different format due to being run in a different pipeline. 

### Metrics

It is common to pay closest attention to F1 measure for NER evaluation. But this depends on the task. For some use cases Precision or Accuracy might be the preferred metric.


### Spacy NER model

I tried two of the larger models: `lg` (large) and `trf` (transformers). (n.b. large is around 700MB, and transformers around 400MB). I would expected that a transformer-based model would be superior and it is so. 

The evaluation metrics SEEM poor for the Spacy model(s). This has more to do with the different in NER classes. Spacy predicts 7+ NER classes while the evaluation on CONLL only compares with 4 classes, and one of those (MISC) is not present in Spacy's classes. I had to convert Spacy labels to CONLL labels where possible. There are inherent "cross dataset generalization" problems in evaluating Spacy on CONLL.

A more accurate way to evaluate Spacy would be to (1) train a customer model on CONLL training data and then (2) evaluate on the test data. I didn't bother to do this. But I do know that people have done this and the accuracy/F1 is around 92%. Spacy isn't SoTA but it is very close out-of-the box


### Flair vs BERT vs Stanford NER Models

| Flair F1 | Bert F1 | Stanford F1 |
| -------- | ------- | ----------- |
| 0.8535   | 0.4140  | 0.9024      |


| Flair Acc | Bert Acc | Stanford Acc |
| --------- | -------- | ------------ |
| 0.9658    | 0.9066   | 0.9758       |


These comparative results are surprising. The Flair model was SoTA (at the top of the NER leaderboard) when it was released a few years ago. The Stanford model has been a good NER model for some time, but I think it is actually quite old.

Stanford uses old technologies - loading Java jar files (trained on Mallet) into NLTK library. Flair on the other hand is very up-to-date - trained on PyTorch using transformer models. I think there might be something going on with "cross dataset generalization" problems here too. My intuition is that Flair SHOULD be the best. 

BERT based NLP models have wide applicability. The NER tagger for BERT is ok out-of-the-box, but this model really requires fine-tuning to get great evaluation metrics. 


### Qualitative Evaluation

Given that there is no labels for CNN data, we can always manually examine a small number of articles to get a sense for how the NER tagger is performing

see
- [CNN_first_10.jsonl](data/processed/cnn_first_10.jsonl)

There are some issues with the NER tagging:

"Kingsbarns"
- tagged as both "FAC" and "GPE"
- should be an ORG

"nine-under", "seven-under", "four-under
- tagged as "QUANTITY" ... I'm not sure these are correct, but I don't quite understand the meaning in golf.

"Carnoustie"
- tagged as "FAC"
- should be LOCATION I think

"24-year-old", "46-year-old"
- tagged as "DATE" but that seems wrong to me

"between three and seven years old"
- tagged as "DATE" - seems wrong

"the night of November 1,"
- tagged as "TIME" - should probably be DATE


Overall the NER tags look pretty good. I am quite impressed actually. 

I've already said that the evaluation on CONLL data is problematic. But there may still be some takeaways about the comparative tagging performance. 
see: [Evaluation_results_spacy_trf.txt](data/interim/evaluation_results_spacy_trf.txt)

This evaluation shows that of the 3 classes with overlap with the CONLL classes, PERSON has much higher Precision and F1 measures than ORGANIZATION and LOCATION. LOCATION has the lowest score of the three. 


### Error Analysis

As noted above the Spacy evaluation shows that LOCATION performed poorly. This may be due to Spacy tagging locations with GPE, FAC, NORP, etc instead. Spacy uses a much richer class of location entities. 

Other than that I see a few DATE and TIME tags that I find questionable. (see above) I may be wrong on these. Similarly with the golf-related "number-under" being tagged as QUANTITY. It seems wrong to me ... but I'm not sure.

I have read that FAC (i.e. Facility) is a tag which was in Spacy's training data erroneously and should be something else. 
see: [FAC in named entities](https://github.com/explosion/spaCy/issues/229)

A post-processing step could be added to re-cast FAC to something else. 

Unfortunately Spacy recommends training from scratch rather than fine tuning their TRF model. This is probably no feasible so better to identify problematic tags and address through post-processing if possible, or move to a more extensible model if the issues are significant.

Both BERT and Flair models can be fine-tuned to improve performance and mitigate such errors. 


------------------------------------------------------------------

## Entity Disambiguation / Linking Entities

I'm not aware of any library/model/approach that can link entities to Wikipedia out of the box. (I might be ignorant about this thought.)

### POC implementation

This is the closest thing I am aware of:
- [Named Entity Disambiguation | HuggingFace](https://huggingface.co/models?other=named-entity-disambiguation)

I added an implemention using one of the Facebook models in the file
- [entity_linking.py](ner4news/entity_linking.py)

But have not integrated it into the pipeline since it will vastly increase processing time and computational expense - the model is 1.63GB and really should be run on a GPU.

### Other approaches to entity disambiguation / linking entities

In the past I have built an ontology (basically a big graph) for entity disambiguation use. The basic approach is to use a structured data knowledgebase (e.g. Wikidata, not Wikipedia), process it to extract the kinds of info you need/want, throw away the rest, and construct a tree. In the end you have something like [Wordnet](https://wordnet.princeton.edu) where you can look up an entity and get a link to a Wikipedia page (or a concept or whatever). YouTube used exactly this approach in the early days to do auto-categorization of videos (based on entities in the text description.)

These kind of ontologies are either (1) very bespoke or (2) valuable so not something organizations give away. (e.g. ConceptWeb was a concept ontology created by Microsoft but only used internally.)



## On Improving Performance / Advanced Techniques

One can fine-tune BERT NER model to vastly improve performance. One of the top-ranked NER models in the past few years takes exactly this approach. 

This notebook:
- [Custom_Named_Entity_Recognition_with_BERT.ipynb](https://github.com/NielsRogge/Transformers-Tutorials/blob/master/BERT/Custom_Named_Entity_Recognition_with_BERT.ipynb)

gives a good overview of fine-tuning a BERT model. This approach requires having/using a labeled dataset. (Goes without saying a lot of data is needed as well.)

It might be possible to fine-tune on OntoNotes dataset to improve performance. (Would have to experiement with this.) Most NLP papers use open datasets so there may be other alternate data sources that could be used for labeled data. Otherwise, most of the effort for improving a model's performance would actually be in labeling a large amount of data to use within a fine-tuning pipeline. 
