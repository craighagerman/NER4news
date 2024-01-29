import gzip
import json
import os
import sys
from pathlib import Path
from zipfile import ZipFile

from obj.cnn_article import CNNArticle
from obj.cnn_article_parser import CNNArticleParser
from tqdm import tqdm
from util.base_logger import log
from util.io import save_gzip

CWD = Path(__file__).parent
PROJECT_DIR = CWD.parent
RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
INTERIM_DIR = os.path.join(PROJECT_DIR, "data", "interim")


class Preprocess:
    def execute(self, data_path):
        log.info("loading CNN data from zip file...")
        jdata = self.load_zipped_data(data_path)
        log.info("deserializing JSON data...")
        articles = self.deserialize(jdata)
        log.info("persisting pre-processed data...")
        self.persist_articles(articles)
        return articles

    def load_zipped_data(self, data_path: str) -> list[dict]:
        """Load cnn_data.zip file and return json data"""
        with ZipFile(data_path, "r") as zip:
            namelist = zip.namelist()
            return json.load(zip.open(namelist[0]))

    def deserialize(self, jdata: list[dict]) -> list[CNNArticle]:
        """Deserialize input json into enriched dataclass data structures"""
        parser = CNNArticleParser()
        return [parser.parse(x) for x in tqdm(jdata)]

    def persist_articles(self, articles: list[CNNArticle]):
        """save processed data to interim directory as a json lines files"""
        jarticles = [json.dumps(obj.to_json()) for obj in articles]
        jl_outpath = os.path.join(INTERIM_DIR, "cnn_articles.jsonl.gzip")
        save_gzip(jl_outpath, jarticles)

        bodytext = [x.body for x in articles]
        txt_outpath = os.path.join(INTERIM_DIR, "cnn_body.txt.gzip")
        save_gzip(txt_outpath, bodytext)


################################################################################
if __name__ == "__main__":

    def usage_msg(msg):
        file_name = os.path.basename(__file__)
        return f"{msg} \nUSAGE: $ python {file_name} <path_to_input_data>"

    args = sys.argv
    if len(args) < 2:
        log.error(usage_msg("Input data not specified."))
    elif len(args) > 2:
        log.error(usage_msg("Too many arguments."))
    else:
        prep = Preprocess()
        prep.execute(args[1])
