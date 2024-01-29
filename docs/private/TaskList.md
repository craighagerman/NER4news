# Task List for takehome assignment


## Environment
- [ ] Decide on Python environment approach (pip only, pyenv, virtualenv conda, Poetry) and implement
- [ ] (OPTIONAL) add in pre-commit hooks
- [ ] (OPTIONAL) implement the entire pipeline as a Docker container (if doable and robust in a limited time)


## Data Exploration
- [ ] look for any mention, write-ups about the CNN news dataset online, make notes on the comments, then re-write in my own words
- [ ] Do EDA in Jupyter notebook. Generate tables & charts
- [ ] Make notes (based on above) on what data cleaning & wrangling is needed


## Pipeline
- [ ] Research what people are using these days for data processing pipelines
- [ ] Set up a data processing pipeline to run everything from start-to-end


## Data Preprocessing
- [ ] create Jupyter notebook, and dedicated module for data cleaning, wrangling & prepocessing. Add the module to a pipeline


## NER approaches
- [ ] research/explore SOTA approaches & frameworks for NER (inc. Spacy, NLTK, Kaggle, github, paperswithcode, etc)
    - [ ] Note the entity coverage of each of the above. e.g. does it handle "quantities, monetary values, percentages" 
- [ ] create an NER python module
- [ ] re-implement NER approaches (in my own style)


## Evaluation
- [ ] Research what is Standard procedure for evaluating NER (precision? other?)
- [ ] Create document (or append) to explain (1) how NER models are evaluated, (2) approaches I am using and (3) why I can't evaluate on CNN (no labels) and (4) implications viz cross data set generalization. Also (5) include discussion of approaches that could be taken to validate the generalization assumptions
- [ ] create a module and Jupyter notebook for running evaulation

### Evaluation Data
- [ ] find and download labeled data for evaluation purposes. Save in `external` data directory.

## Error Analysis
- I'm not 100% sure that this means / should involve. I think this is just the "discussion" part of Evaluation.
- [ ] research examples of "error analysis" for NER or for NLP in general and model those approaches


## Code Quality
- [ ] Create a document to describe my philsophy about coding best practices and explain/describe differences between ML/DS and SE and explain how I AM folling best practices for my field. 


## Bonus
- [ ] research/look into what ELSE people do around NER that I could also implement / add in as an extension. 

## Bonus: Entity disambiguation OR linking entities
- [ ] Research if these are the same or different, what approaches are generally used and if there is anything tractable / doable for this take home assignment. Otherwise, write notes to (1) describe approach and (2) architecture and include as a discussion.


--------------------------------------------------------------------------------------------------------------

## Ideas for extras

EDA & manual validation
- [ ] Create a Jupyter notebook for (1) exploring the dataset before modeling (randomly select & display rows of data, maybe some kind of simple keyword search, maybe query expansion search, semantic search) and for (2) exploring the labeled data post-annotation. Allow for searching & displaying by entity type
    - [ ] AND/OR Do something like above but using an API and frontend


API extension
- [ ] Write an API (fastAPI) for returning NER entities for a given document. Have routes for either (1) passing in a document or (2) specifying a URL for a news article (have newspaper3k extract the body and return the NER entitites)







