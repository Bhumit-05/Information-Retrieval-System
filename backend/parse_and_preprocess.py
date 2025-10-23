# parse_and_preprocess.py
import json
import pandas as pd
import os

# --- Import our new modules ---
from config import OUTPUT_DATA_DIR, DOCS_JSON, QUERIES_JSON, QRELS_JSON
from parsers import parse_docs, parse_queries, parse_qrels
from preprocessing import preprocess


# --- 4. Main Execution ---

def main():
    # 0. Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DATA_DIR):
        os.makedirs(OUTPUT_DATA_DIR)
        print(f"Created directory: {OUTPUT_DATA_DIR}")

    # 1. Parse all raw files (using functions from parsers.py)
    docs = parse_docs()
    queries = parse_queries()
    qrels = parse_qrels()
    
    if not docs or not queries or not qrels:
        print("Error during parsing. Exiting.")
        return

    # 2. Process documents
    print("\nPreprocessing documents...")
    
    # We will use pandas DataFrame for easy processing
    df_docs = pd.DataFrame(docs)
    
    # Show an example BEFORE preprocessing (as you requested)
    print("\n--- PREPROCESSING EXAMPLE ---")
    print(f"DOC ID: {df_docs.iloc[0]['doc_id']}")
    print(f"\nORIGINAL TEXT:\n{df_docs.iloc[0]['full_text'][:250]}...")
    
    # Apply the preprocessing function (imported from preprocessing.py)
    # 'processed_text' will be the input to our TF-IDF model
    df_docs['processed_text'] = df_docs['full_text'].apply(preprocess)
    
    # Show the SAME example AFTER preprocessing
    print(f"\nPROCESSED TEXT:\n{df_docs.iloc[0]['processed_text'][:250]}...")
    print("-----------------------------\n")

    # 3. Save processed data
    
    # Convert DataFrame back to list of dicts for JSON
    processed_docs_list = df_docs.to_dict('records')
    
    # Use path constants from config.py
    with open(DOCS_JSON, 'w') as f:
        json.dump(processed_docs_list, f, indent=2)
    print(f"Saved processed documents to {DOCS_JSON}")

    with open(QUERIES_JSON, 'w') as f:
        json.dump(queries, f, indent=2)
    print(f"Saved queries to {QUERIES_JSON}")

    with open(QRELS_JSON, 'w') as f:
        json.dump(qrels, f, indent=2)
    print(f"Saved qrels to {QRELS_JSON}")
    
    print("\nPhase 1 complete! All processed data is in the 'backend/data' folder.")

if __name__ == "__main__":
    main()