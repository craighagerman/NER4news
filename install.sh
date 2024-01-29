

# Optional Install 

# Install desired Spacy model(s)
# This was specified in the Readme Getting Started instructions so probably not necessary here. 
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_trf


# If using Stanford NER model it needs to be downloaded. 
# this is done in the Jupyter notebook but sometimes fails there.
wget http://nlp.stanford.edu/software/stanford-ner-2015-04-20.zip
unzip stanford-ner-2015-04-20.zip
