import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz 
from config import DOCS_JSON, VECTORIZER_PATH, TFIDF_MATRIX_PATH, DOC_LOOKUP_PATH

try:
    with open(DOCS_JSON, 'r') as f:
        docs = json.load(f)
except FileNotFoundError:
    print(f"Error: {DOCS_JSON} not found.")
    exit()

corpus = []
doc_lookup = {} # {doc_id: {title, text}}

for doc in docs:
    corpus.append(doc['processed_text'])
    
    doc_lookup[doc['doc_id']] = {
        'title': doc['title'],
        'text': doc['text']
    }

vectorizer = TfidfVectorizer(min_df=5, max_df=0.95)

tfidf_matrix = vectorizer.fit_transform(corpus)

print(f"TF-IDF matrix created!")

with open(VECTORIZER_PATH, 'wb') as f_vec:
    pickle.dump(vectorizer, f_vec)

save_npz(TFIDF_MATRIX_PATH, tfidf_matrix)

with open(DOC_LOOKUP_PATH, 'w') as f_lookup:
    json.dump(doc_lookup, f_lookup, indent=2)

print("\nIndex Built!")