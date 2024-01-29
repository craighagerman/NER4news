

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from obj.cnn_article import CNNArticle
from tqdm import tqdm
from util.base_logger import log


class EntityLinking:
    def __init__(self):
        """
            Use a pre-trained Hugging Face PyTorch model to extract the 'genre'
            for use in entity disambiguation. 

            Two choices of model:
            - https://huggingface.co/facebook/genre-kilt
            - https://huggingface.co/facebook/mgenre-wiki
        """
        model = "facebook/genre-kilt"
        model = "facebook/mgenre-wiki"
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model).eval()

    def execute(self, articles: list[CNNArticle]):
        log.info("Extracting entities from articles...")
        articles = [self.enrich(x) for x in tqdm(articles)]
        return articles

    def enrich(self, article: CNNArticle) -> CNNArticle:
        """Enrich Article object with entity data"""
        entities = self.extract_genre(article.body)
        article.entities = entities
        return article


    def extract_genre(self, text) -> dict[str, list]:
        """Use HuggingFace genre-kilt model to perform entity linking"""

        sentences = [text]
        outputs = self.model.generate(
            **self.tokenizer(sentences, return_tensors="pt"),
            num_beams=5,
            num_return_sequences=5
        )
        predictions = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return {"linked_entities": predictions}
