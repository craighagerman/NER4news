import json
import os
import random
import shutil
import sys
import time
from pathlib import Path

from ner import NER
from preprocess import Preprocess
from util.base_logger import log
from util.io import save_gzip, load_gzip_articles

CWD = Path(__file__).parent
PROJECT_DIR = CWD.parent
INTERIM_DIR = os.path.join(PROJECT_DIR, "data", "interim")
PROCESSED_DIR = os.path.join(PROJECT_DIR, "data", "processed")


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        duration = te - ts
        duration = float(f"{duration:.2f}")
        log.info(f"Running time: {duration} sec ")
        return result

    return timed


@timeit
def main(input_path):
    articles = Preprocess().execute(input_path)
    articles = NER().execute(articles)
    outpath = os.path.join(PROCESSED_DIR, "cnn_articles_w_entities.jsonl.gzip")
    log.info(f"Saving NER-enriched articles to {outpath}...")
    jarticles = [json.dumps(obj.to_json()) for obj in articles]
    save_gzip(outpath, jarticles)

    # Extract 10 random articles for sanity-check evaluation
    sample = [
        {"body": x.body, "entities": x.entities} for x in random.sample(articles, 10)
    ]
    sample_outpath = os.path.join(PROCESSED_DIR, "cnn_article_sample.jsonl")
    with open(sample_outpath, "w") as fo:
        fo.write(json.dumps(sample, indent=2))


@timeit
def firstN(input_path, num):
    num = int(num)
    try:
        inpath = os.path.join(INTERIM_DIR, "cnn_articles.jsonl.gzip")
        articles = load_gzip_articles(inpath)
    except FileNotFoundError:
        articles = Preprocess().execute(input_path)
    articles = NER().execute(articles[:num])
    sample = [{"body": x.body, "entities": x.entities} for x in articles]
    outpath = os.path.join(PROCESSED_DIR, f"cnn_first_{num}.jsonl")
    log.info(f"Saving first 10 NER-enriched articles to {outpath}...")
    with open(outpath, "w") as fo:
        fo.write(json.dumps(sample, indent=2))


# ------------------------------
if __name__ == "__main__":

    def usage_msg(msg):
        file_name = os.path.basename(__file__)
        return (
            f"{msg} \nUSAGE: $ python {file_name} <path_to_input_data> [num_of_records]"
        )

    args = sys.argv
    if len(args) < 2:
        log.error(usage_msg("Input data not specified."))
    elif len(args) > 3:
        log.error(usage_msg("Too many arguments."))
    elif len(args) == 2:
        main(args[1])
    elif len(args) == 3:
        firstN(args[1], args[2])
