import spacy
from obj.cnn_article import CNNArticle
from tqdm import tqdm
from util.base_logger import log


class NER:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")

    def execute(self, articles: list[CNNArticle]):
        log.info("Extracting entities from articles...")
        articles = [self.enrich(x) for x in tqdm(articles)]
        return articles

    def enrich(self, article: CNNArticle) -> CNNArticle:
        """Enrich Article object with entity data"""
        entities = self.extract_entities(article.body)
        article.entities = entities
        return article

    def extract_entities(self, text) -> dict[str, list]:
        """Use SpaCy to extract entities from text. Return as a dict[str, list]"""
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return {"entities": entities}
