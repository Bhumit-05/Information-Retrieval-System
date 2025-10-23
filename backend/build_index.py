# build_index.py
import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz # Used for saving the sparse matrix

# --- 1. Configuration (Import from config.py) ---
from config import DOCS_JSON, VECTORIZER_PATH, TFIDF_MATRIX_PATH, DOC_LOOKUP_PATH

# Define file paths
DOCS_JSON_PATH = DOCS_JSON # Keep variable name consistent with old script


# --- 2. Load Processed Documents ---

print(f"Loading processed documents from {DOCS_JSON_PATH}...")
try:
    with open(DOCS_JSON_PATH, 'r') as f:
        docs = json.load(f)
except FileNotFoundError:
    print(f"Error: {DOCS_JSON_PATH} not found.")
    print("Please run '1_parse_and_preprocess.py' first.")
    exit()

# --- 3. Prepare Data for TF-IDF ---

# The TfidfVectorizer requires two things:
# 1. A 'corpus': A list of strings (the text of each document).
# 2. A 'lookup': A way to map the results (which are matrix row indices) back to our doc_ids.

corpus = []
doc_lookup = {} # This will be our {doc_id: {title, text}} mapping

for doc in docs:
    corpus.append(doc['processed_text'])
    
    # Store the info our API will need to display results
    doc_lookup[doc['doc_id']] = {
        'title': doc['title'],
        'text': doc['text'],
        'full_text': doc['full_text'] # Store full text for the /doc/{id} endpoint
    }

print(f"Created corpus with {len(corpus)} documents.")
print(f"Created doc_lookup with {len(doc_lookup)} entries.")


# --- 4. Initialize and Fit TF-IDF Vectorizer ---

# Here, we are using the default settings for TfidfVectorizer.
# - It handles tokenization (splitting) by whitespace.
# - It uses its own internal lowercase and accent stripping.
# - It calculates TF and IDF and L2-normalizes the resulting vectors.
# Since we've already done our own advanced preprocessing (lemmatization, stopwords),
# our input 'corpus' is already just a string of clean tokens.
#
# For your project report, you could also pass in your 'preprocess' function
# directly to TfidfVectorizer using the 'tokenizer' or 'analyzer' argument,
# but loading the pre-processed text is simpler and more efficient.

print("Initializing TfidfVectorizer...")
# We can set min_df=5 to ignore terms that appear in fewer than 5 docs
# and max_df=0.95 to ignore terms that appear in more than 95% of docs.
# This is a common way to remove noise.
vectorizer = TfidfVectorizer(min_df=5, max_df=0.95)

print("Fitting TF-IDF model to the corpus...")
# .fit_transform() does two things:
# 1. 'fit': It learns the vocabulary and IDF weights.
# 2. 'transform': It converts our corpus into the TF-IDF document-term matrix.
tfidf_matrix = vectorizer.fit_transform(corpus)

print(f"TF-IDF matrix created with shape: {tfidf_matrix.shape}")
# The shape is (number of documents, number of unique vocabulary words)
# e.g., (1400, 3163) means 1400 docs and 3163 unique words (after min/max_df)


# --- 5. Save the Model and Lookup Files ---

# 1. Save the fitted TfidfVectorizer
# This object *is* our model. It contains the vocabulary and IDF weights.
# We need it to transform new queries.
print(f"Saving TfidfVectorizer to {VECTORIZER_PATH}...")
with open(VECTORIZER_PATH, 'wb') as f_vec:
    pickle.dump(vectorizer, f_vec)

# 2. Save the TF-IDF matrix
# This is the matrix of all document vectors. We compare our query vector against this.
print(f"Saving TF-IDF matrix to {TFIDF_MATRIX_PATH}...")
save_npz(TFIDF_MATRIX_PATH, tfidf_matrix)

# 3. Save the document lookup dictionary
# This is for our API to quickly fetch doc details.
print(f"Saving document lookup to {DOC_LOOKUP_PATH}...")
with open(DOC_LOOKUP_PATH, 'w') as f_lookup:
    json.dump(doc_lookup, f_lookup, indent=2)

print("\nPhase 2 complete! Model and data files are saved in 'backend/data/'.")