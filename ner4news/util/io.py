import gzip
import json
import os

from obj.cnn_article import CNNArticle
from util.base_logger import log


def save_gzip(outpath, data):
    log.info(f"Saving gzip data to {outpath}...")
    with gzip.open(outpath, "wt") as fo:
        fo.write("\n".join(data))


def load_gzip_articles(inpath):
    log.info(f"Loading gzip data from {inpath}...")
    raw = [json.loads(x) for x in gzip.open(inpath, "rt")]
    articles = [CNNArticle(**x) for x in raw]
    return articles
