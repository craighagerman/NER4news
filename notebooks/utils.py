
from typing import List, Tuple
import json
import os
import re
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')  # "error", "ignore", "always", "default", "module" or "once"

# Huggingface datasets is needed to load the CONLL 2003 data
from datasets import load_dataset, Dataset
# A Hugging library for easily evaluating machine learning models and datasets.
import evaluate


# Load the CONLL 2003 dataset
conll = load_dataset("conll2003")
tag_names = conll["test"].features[f"ner_tags"].feature.names
test = conll["test"]


interim_dir = "../data/interim"
external_dir = "../data/external"

conll_dir = os.path.join(external_dir, "archive")

test_data_path = os.path.join(conll_dir, "test.txt")


########################################
# I/O Helper Functions
########################################
def _load_persisted_json(inpath: str) -> dict:
    return json.loads(open(inpath).read())

def save_ner_results(outpath: str, references: list[list[str]], predictions: list[list[str]]) -> None:
    """ Helper function for persisting true and predicted NER labels """
    print(f"Saving NER results to {outpath}")
    d = {"references": references, "predictions": predictions}
    with open(outpath, "w") as fo:
        fo.write(json.dumps(d))

def load_ner_results(inpath: str) -> Tuple[list[list[str]], list[list[str]]]:
    """ Helper function for loading previously persisted true and predicted NER labels """
    d = json.loads(open(inpath).read())
    return d["references"], d["predictions"]


def evaluate_results(references: list[list[str]], predictions: list[list[str]]):
    seqeval = evaluate.load("seqeval")
    return seqeval.compute(predictions=predictions, references=references)

def save_evaluation_results(outpath: str, results: dict) -> None:
    print(f"Saving evaluation results to {outpath}")
    with open(outpath, "w") as fo:
        # fo.write(json.dumps(results))
        fo.write(json.dumps(results, indent=2, default=float))

def load_evaluation_results(inpath: str) -> dict:
    return _load_persisted_json(inpath)



if __name__ == "__main__":
    print(conll_dir)