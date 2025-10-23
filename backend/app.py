# app.py
import json
import pickle
from nltk.corpus import stopwords
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Import from our new modules ---
from config import VECTORIZER_PATH, TFIDF_MATRIX_PATH, DOC_LOOKUP_PATH
from preprocessing import preprocess


# --- 1. Initialize Flask App & CORS ---
app = Flask(__name__)
# Enable CORS (Cross-Origin Resource Sharing)
# This allows your React frontend (on a different port) to make requests to this backend.
CORS(app)


# --- 2. Load Models and Data (One-time setup) ---
print("Loading models and data... This may take a moment.")
# Note: nlp and stop_words are loaded by config.py,
# which is used by preprocessing.py. We just need data files here.

# Define file paths (using imported constants)
VECTORIZER_PATH = VECTORIZER_PATH
TFIDF_MATRIX_PATH = TFIDF_MATRIX_PATH
DOC_LOOKUP_PATH = DOC_LOOKUP_PATH

# Load the models
try:
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open(DOC_LOOKUP_PATH, 'r') as f:
        doc_lookup = json.load(f)
        
    tfidf_matrix = load_npz(TFIDF_MATRIX_PATH)
    
    # We need a mapping from the tfidf_matrix row index back to our doc_id
    # Since we built the matrix from the list of docs in order,
    # the keys of doc_lookup (which were added in order) correspond to the rows.
    # We create a list of doc_ids in the matrix order.
    index_to_doc_id = list(doc_lookup.keys())

except FileNotFoundError:
    print("Error: Model files not found. Please run '1_parse_and_preprocess.py' and '2_build_index.py' first.")
    exit()

# Load spaCy and NLTK stopwords (also one-time)
# --- THIS SECTION IS NO LONGER NEEDED ---
# try:
#     nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
# except IOError:
#     print("Spacy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
#     exit()
# stop_words = set(stopwords.words('english'))
# --- END DELETED SECTION ---

print("Models and data loaded successfully.")


# --- 3. Preprocessing Function (Copied from Phase 1) ---
# --- THIS FUNCTION IS NO LONGER NEEDED ---
# We import it from preprocessing.py
# def preprocess(text):
#     ...
# --- END DELETED SECTION ---


# --- 4. Define API Endpoints ---

@app.route('/search', methods=['GET'])
def search():
    """
    Handles the /search?q=...&k=... endpoint.
    """
    # Get query and k from URL parameters
    query_text = request.args.get('q', '')
    k = int(request.args.get('k', 10)) # Default to 10 results

    if not query_text:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    # 1. Preprocess the query (using imported function)
    processed_query = preprocess(query_text)

    # 2. Transform the query into a TF-IDF vector
    # We use .transform() on the *loaded* vectorizer
    # Note: .transform() expects a list of documents, so we pass [processed_query]
    query_vector = vectorizer.transform([processed_query])

    # 3. Calculate Cosine Similarity
    # This computes the similarity between our 1 query vector and all 1400 doc vectors
    cosine_sims = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # 4. Get Top-K results
    # Get the indices of the top-k scores
    # argsort() gives indices that would sort the array,
    # [-k:] gets the last k (highest scores),
    # [::-1] reverses them to be in descending order.
    top_k_indices = cosine_sims.argsort()[-k:][::-1]

    # 5. Format the results
    results = []
    for idx in top_k_indices:
        doc_id = index_to_doc_id[idx] # Map matrix index back to doc_id
        doc = doc_lookup[doc_id]
        score = float(cosine_sims[idx]) # Convert numpy.float to standard float for JSON
        
        # Create snippet
        snippet = doc['text'][:150] + '...' # Get first 150 chars
        
        results.append({
            'doc_id': doc_id,
            'title': doc['title'],
            'snippet': snippet,
            'score': score
        })

    return jsonify(results)


@app.route('/doc/<string:doc_id>', methods=['GET'])
def get_document(doc_id):
    """
    Handles the /doc/{id} endpoint.
    """
    # Look up the document by its ID
    doc_data = doc_lookup.get(doc_id)
    
    if doc_data:
        # Return the full document data (title, full_text, metadata)
        return jsonify(doc_data)
    else:
        return jsonify({"error": "Document not found"}), 404


# --- 5. Run the App ---
if __name__ == '__main__':
    # Setting debug=True gives you helpful error messages
    # and auto-reloads the server when you save changes.
    app.run(debug=True, port=5000)