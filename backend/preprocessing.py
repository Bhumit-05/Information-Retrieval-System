from config import nlp

def preprocess(text):
    # Normalizing, tokenizing, removing stopwords, and lemmatizing text.

    doc = nlp(text)
    
    tokens = []
    for tok in doc:
        if not tok.is_stop and not tok.is_punct:
            token_clean = tok.lemma_.lower().strip()
            if token_clean:
                tokens.append(token_clean)
                
    return " ".join(tokens)