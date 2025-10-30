# app.py
import json
import pickle
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import VECTORIZER_PATH, TFIDF_MATRIX_PATH, DOC_LOOKUP_PATH
from preprocessing import preprocess


app = Flask(__name__)
CORS(app)

try:
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open(DOC_LOOKUP_PATH, 'r') as f:
        doc_lookup = json.load(f)
        
    tfidf_matrix = load_npz(TFIDF_MATRIX_PATH)
    
    index_to_doc_id = list(doc_lookup.keys())

except FileNotFoundError:
    print("Error: Model files not found. Run parse_and_preprocess.py and build_index.py")
    exit()

@app.route('/search', methods=['GET'])
def search():
    query_text = request.args.get('q', '')
    k = int(request.args.get('k', 10))

    if not query_text:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    processed_query = preprocess(query_text)

    query_vector = vectorizer.transform([processed_query])

    cosine_sims = cosine_similarity(query_vector, tfidf_matrix).flatten()

    top_k_indices = cosine_sims.argsort()[-k:][::-1]


    results = []
    for idx in top_k_indices:
        doc_id = index_to_doc_id[idx]
        doc = doc_lookup[doc_id]
        score = float(cosine_sims[idx])
        
        snippet = doc['text'][:150] + '...'
        
        results.append({
            'doc_id': doc_id,
            'title': doc['title'],
            'snippet': snippet,
            'score': score
        })

    return jsonify(results)


@app.route('/doc/<string:doc_id>', methods=['GET'])
def get_document(doc_id):
    doc_data = doc_lookup.get(doc_id)
    
    if doc_data:
        return jsonify(doc_data)
    else:
        return jsonify({"error": "Document not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)