# config.py
import spacy
import json
import re
from nltk.corpus import stopwords
import pandas as pd
import os

# --- 1. Configuration ---

print("Loading spaCy model and NLTK stopwords...")

# Load the small English model for spaCy
# We disable 'parser' and 'ner' for speed since we only need tokenization and lemmatization
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
except IOError:
    print("Spacy model 'en_core_web_sm' not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    exit()

# Load NLTK stopwords
stop_words = set(stopwords.words('english'))
print("Models loaded successfully.")


# --- Define File Paths ---

# Define file paths (relative to this script in the 'backend' folder)
DOCS_FILE = 'cran.all.1400'
QUERIES_FILE = 'cran.qry'
QRELS_FILE = 'cranqrel'

# Define output paths
# We'll put processed data in a 'data' sub-directory for cleanliness
OUTPUT_DATA_DIR = 'data'
DOCS_JSON = os.path.join(OUTPUT_DATA_DIR, 'cranfield_docs.json')
QUERIES_JSON = os.path.join(OUTPUT_DATA_DIR, 'cranfield_queries.json')
QRELS_JSON = os.path.join(OUTPUT_DATA_DIR, 'cranfield_qrels.json')

# --- Define Index/Model Paths ---
VECTORIZER_PATH = os.path.join(OUTPUT_DATA_DIR, 'tfidf_vectorizer.pkl')
TFIDF_MATRIX_PATH = os.path.join(OUTPUT_DATA_DIR, 'tfidf_matrix.npz')
DOC_LOOKUP_PATH = os.path.join(OUTPUT_DATA_DIR, 'doc_lookup.json')