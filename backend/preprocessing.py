# preprocessing.py

# Import models from our new config file
from config import nlp, stop_words

# --- 2. Preprocessing Function (Your Requirement) ---

def preprocess(text):
    """
    Normalizes, tokenizes, removes stopwords, and lemmatizes text.
    """
    # Use spaCy's nlp pipeline
    doc = nlp(text) 
    
    tokens = []
    for tok in doc:
        # 1. Check if it's not a stopword or punctuation
        if not tok.is_stop and not tok.is_punct:
            # 2. Clean, lowercase, and lemmatize
            token_clean = tok.lemma_.lower().strip()
            # 3. Ensure it's not an empty string after stripping
            if token_clean:
                tokens.append(token_clean)
                
    # Join tokens back into a single string for TfidfVectorizer
    return " ".join(tokens)