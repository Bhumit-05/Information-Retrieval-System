import json
import os
from config import OUTPUT_DATA_DIR, DOCS_JSON
from parsers import parse_docs
from preprocessing import preprocess

def main():
    if not os.path.exists(OUTPUT_DATA_DIR):
        os.makedirs(OUTPUT_DATA_DIR)

    
    docs = parse_docs()
    
    for doc in docs:
        processed_text = preprocess(doc['text'])
        doc['processed_text'] = processed_text
    
    with open(DOCS_JSON, 'w') as f:
        json.dump(docs, f, indent=2)
        
    
    print("\nData Processed!")

if __name__ == "__main__":
    main()