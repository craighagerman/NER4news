# Notes on take home assignment


## Objective
Develop a Named Entity Recognition (NER) system to identify and classify entities such as names of people, organizations, locations, expressions of times, quantities, monetary values, percentages, etc., from a collection of news articles.

> [!Note] NER applications often/typically are about people, organizations, locations only. Other mentioned entities may not be covered by some libraries/approachs. Also "percentages" is just vague.



## Task Description:
1. Data Preparation:
- use CNN news article dataset. It should contains a diverse range of articles from various news sources and topics.
    - comment: false assumption. It is from CNN only, not from "various news sources"
- Perform necessary data cleaning and text processing

2. Model Development:
- Implement an NER model using any NLP techniques or framework (e.g., CRF, SpaCy, BERT-based models).
- Explain the choice of model and its architecture

3. Model Evaluation:
- Evaluate the model using appropriate metrics (e.g.,Precision,Recall, F1-Score at the entity level).
- Proviate analyis on the model's performance across different entity types.

4. Error Analysis:
- Conduct error analysis to identify the types of errors the model is making
- Suggest potential improvemewnts or strategies to address these errors

5. Code Quality and Documentation:
- Ensure the code is well-organized, documented and easily runnable
- Include a README file with instructions on how to set up and run the project and any necessary environment setup

6. Bonus (Optional):
- Extend the model to handle entity disambiguation or linking entities to a knowledgebase (e.g. Wikipedia)
- Explore and implement advanced techniques or models to improve performance


## Sample Data Set: CNN News Data Set from data.world
https://data.world/opensnippets/cnn-news-dataset


## Deliverables:
-  Source code.
-  A detailed report documenting the approach, evaluation results, and error analysis.
-  (If attempted) Additional features or advanced implementations.

