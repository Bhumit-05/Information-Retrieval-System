import re
from config import DOCS_FILE

def parse_docs():
    #.I (ID), .T (Title), .A (Author), .B (Bib), .W (Text)
    
    docs = []
    try:
        with open(DOCS_FILE, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {DOCS_FILE} not found. Make sure it's in the 'backend' directory.")
        return []

    doc_splits = content.split('.I ')[1:]

    for doc_text in doc_splits:
        
        doc_id_match = re.search(r'(\d+)', doc_text) 
        title_match = re.search(r'\.T\n(.*?)\n(\.A|\.B|\.W|$)', doc_text, re.S)
        author_match = re.search(r'\.A\n(.*?)\n\.B', doc_text, re.S)
        bib_match = re.search(r'\.B\n(.*?)\n\.W', doc_text, re.S)
        text_match = re.search(r'\.W\n(.*?)$', doc_text, re.S)

            
        doc_id = doc_id_match.group(1).strip()
        title = title_match.group(1).strip().replace('\n', ' ')
        text = text_match.group(1).strip().replace('\n', ' ')
        author = author_match.group(1).strip().replace('\n', ' ') if author_match else ""
        bib = bib_match.group(1).strip().replace('\n', ' ') if bib_match else ""
        
        docs.append({
            'doc_id': doc_id,
            'title': title,
            'text': text,
            'metadata': {'author': author, 'bib': bib}
        })
        
    print(f"Parsed {len(docs)} documents.")
    return docs