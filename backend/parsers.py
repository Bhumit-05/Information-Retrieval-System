# parsers.py
import re

# Import file path constants from our config file
from config import DOCS_FILE, QUERIES_FILE, QRELS_FILE

# --- 3. Parsing Functions ---

def parse_docs():
    """
    Parses the 'cran.all.1400' file.
    The file format is: .I (ID), .T (Title), .A (Author), .B (Bib), .W (Text)
    """
    print(f"Parsing documents from {DOCS_FILE}...")
    docs = []
    try:
        with open(DOCS_FILE, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {DOCS_FILE} not found. Make sure it's in the 'backend' directory.")
        return []

    # Split the content by the .I marker, which separates documents
    # The first split is empty, so we skip it [1:]
    doc_splits = content.split('.I ')[1:]

    for doc_text in doc_splits:
        # Regex to find the markers. 're.S' (DOTALL) makes '.' match newlines
        doc_id_match = re.search(r'(\d+)', doc_text)
        title_match = re.search(r'\.T\n(.*?)\n\.A', doc_text, re.S)
        author_match = re.search(r'\.A\n(.*?)\n\.B', doc_text, re.S)
        bib_match = re.search(r'\.B\n(.*?)\n\.W', doc_text, re.S)
        text_match = re.search(r'\.W\n(.*?)$', doc_text, re.S)

        if not all([doc_id_match, title_match, text_match]):
            print(f"Skipping a malformed doc entry. Text starts with: {doc_text[:50]}")
            continue
            
        doc_id = doc_id_match.group(1).strip()
        
        # We combine title and text for a richer search index
        title = title_match.group(1).strip().replace('\n', ' ')
        text = text_match.group(1).strip().replace('\n', ' ')
        full_text = title + " " + text # Combine title and text
        
        # Store metadata
        author = author_match.group(1).strip().replace('\n', ' ') if author_match else ""
        bib = bib_match.group(1).strip().replace('\n', ' ') if bib_match else ""
        
        docs.append({
            'doc_id': doc_id,
            'title': title,
            'text': text,
            'full_text': full_text, # We will process this field
            'metadata': {'author': author, 'bib': bib}
        })
        
    print(f"Successfully parsed {len(docs)} documents.")
    return docs

def parse_queries():
    """
    Parses the 'cran.qry' file.
    """
    print(f"Parsing queries from {QUERIES_FILE}...")
    queries = []
    try:
        with open(QUERIES_FILE, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {QUERIES_FILE} not found.")
        return []

    query_splits = content.split('.I ')[1:]

    for q_text in query_splits:
        query_id_match = re.search(r'(\d+)', q_text)
        text_match = re.search(r'\.W\n(.*?)$', q_text, re.S)

        if not query_id_match or not text_match:
            continue
            
        query_id = query_id_match.group(1).strip()
        text = text_match.group(1).strip().replace('\n', ' ')
        
        queries.append({
            'query_id': query_id,
            'text': text
        })
        
    print(f"Successfully parsed {len(queries)} queries.")
    return queries

def parse_qrels():
    """
    Parses 'cranqrel' file into a dictionary.
    Format: "query_id doc_id relevance" (relevance is unused here)
    Output: {"1": ["184", "29", ...], "2": ["39", "156", ...]}
    """
    print(f"Parsing relevance judgments (qrels) from {QRELS_FILE}...")
    qrels = {}
    try:
        with open(QRELS_FILE, 'r') as f:
            for line in f:
                # Split on whitespace
                parts = line.split()
                if len(parts) < 2:
                    continue
                    
                query_id = parts[0]
                doc_id = parts[1]
                
                if query_id not in qrels:
                    qrels[query_id] = []
                qrels[query_id].append(doc_id)
    except FileNotFoundError:
        print(f"Error: {QRELS_FILE} not found.")
        return {}
            
    print(f"Successfully parsed qrels for {len(qrels)} queries.")
    return qrels