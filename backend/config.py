import spacy
from nltk.corpus import stopwords
import os

nlp = spacy.load("en_core_web_sm")


DOCS_FILE = 'cran.all.1400'
OUTPUT_DATA_DIR = 'data'
DOCS_JSON = os.path.join(OUTPUT_DATA_DIR, 'cranfield_docs.json')

VECTORIZER_PATH = os.path.join(OUTPUT_DATA_DIR, 'tfidf_vectorizer.pkl')
TFIDF_MATRIX_PATH = os.path.join(OUTPUT_DATA_DIR, 'tfidf_matrix.npz')
DOC_LOOKUP_PATH = os.path.join(OUTPUT_DATA_DIR, 'doc_lookup.json')