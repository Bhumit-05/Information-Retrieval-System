# Information Retrieval System - Project Flow

---

## Phase 1: Offline Data Pipeline & Indexing ⚙️

This is the one-time setup process run from the terminal to build all the necessary data and model files.

1.  You run `python 1_parse_and_preprocess.py`.
2.  **Parse Raw Files:** The script reads the raw Cranfield files (`cran.all.1400`, `cran.qry`, `cranqrel`).
3.  **Process Documents:** It loops through all 1400 documents to clean their text.
4.  **Clean Text:** For each document, the following steps are performed:
    * **Tokenization:** The text is lowercased and split into individual words (tokens).
    * **Stopword/Punctuation Removal:** Common words (like "the", "a") and punctuation are removed using **NLTK**.
    * **Lemmatization:** Each remaining word is reduced to its root form (e.g., "running" $\rightarrow$ "run") using **spaCy**.
5.  **Save Processed Data:** The script saves all the cleaned document text, queries, and relevance data into new JSON files (e.g., `cranfield_docs.json`) inside the `/data` folder.
6.  You run `python 2_build_index.py`.
7.  **Load Processed JSON:** This script reads the `cranfield_docs.json` you just created.
8.  **Build Corpus:** It creates a large list (a corpus) containing the processed text string for all 1400 documents.
9.  **Fit & Transform:** The entire corpus is fed into `TfidfVectorizer` (from scikit-learn). This does two things:
    * **Fit:** It learns the complete vocabulary and calculates the IDF (Inverse Document Frequency) weight for every word.
    * **Transform:** It converts all 1400 documents into numerical vectors, creating the final **TF-IDF matrix**.
10. **Save Model:** The script saves the final model and lookup files to the `/data` folder:
    * `tfidf_matrix.npz`: The large matrix of all document vectors.
    * `tfidf_vectorizer.pkl`: The "brain" of the vectorizer (the vocabulary and IDF weights).
    * `doc_lookup.json`: A simple file to get a document's title and text from its ID.

**At this point, the "brain" of your search engine is built and saved to disk.**

---

## Phase 2: Live Application & User Search 🚀

This is what happens when a user visits your website.

1.  **Start Servers:**
    * **Backend:** You run `python app.py` to start the **Flask** server.
    * **Frontend:** You run `npm run dev` to start the **React (Vite)** server.
2.  **Backend Loads Index:** The **Flask** (`app.py`) server starts and immediately loads `tfidf_matrix.npz`, `tfidf_vectorizer.pkl`, and `doc_lookup.json` into memory.
3.  **Backend Runs Evaluation:** The server also runs the full evaluation logic (using `cran.qry` and `cranqrel`) and caches the final **MAP** and **Precision** scores.
4.  **User Visits Site:** A user opens your React app (e.g., `http://localhost:5173`) in their browser.
5.  **User Searches:** The user types a query (e.g., "aerodynamic wing") into the search bar and hits "Search."
6.  **React Sends Request:** The React app sends an API `fetch` request to the Flask server: `GET /search?q=aerodynamic+wing`.
7.  **Flask Cleans Query:** The server receives the query string ("aerodynamic wing") and runs it through the *exact same* **`preprocess`** function (tokenize, remove stopwords, lemmatize).
8.  **Flask Vectorizes Query:** It uses the *loaded* `tfidf_vectorizer` (from the `.pkl` file) to transform the cleaned query string into a single TF-IDF vector.
9.  **Flask Calculates Similarity:** The server uses **`cosine_similarity`** to compare the user's single query vector against all 1400 document vectors stored in the matrix.
10. **Flask Ranks Results:** This comparison produces 1400 similarity scores. The server sorts these scores to find the top-K (e.g., top 100) most relevant document IDs.
11. **Flask Responds:** The server uses `doc_lookup.json` to get the titles and snippets for the top IDs and sends them back to React as a single JSON list.
12. **React Renders UI:** React receives the JSON data, updates its state, and re-renders the page to display the ranked list of search results to the user.









Regex:

All these expressions use `re.search()`, which finds the *first* location in the `doc_text` string where the pattern produces a match.

-----

### 1\. Document ID

```python
doc_id_match = re.search(r'(\d+)', doc_text)
```

  * `r'...'`: This indicates a "raw string" in Python. It tells Python not to interpret backslashes (`\`) as escape characters, which is standard practice for regex patterns.
  * `(\d+)`: This is the core pattern.
      * `\d`: Matches any single digit (0-9).
      * `+`: This is a "quantifier." It means "match one or more of the preceding token" (in this case, one or more digits).
      * `(...)`: The parentheses create a **capturing group**. This means the part of the string that matches the pattern inside the parentheses (the actual digits) will be saved and can be accessed from the match object (e.g., using `doc_id_match.group(1)`).

**In short: This regex finds the first sequence of one or more digits in the text.**

-----

### 2\. Title Match

```python
title_match = re.search(r'\.T\n(.*?)\n\.A', doc_text, re.S)
```

  * `\.T\n`: This matches the literal characters `.T` followed by a newline (`\n`). The backslash before the dot (`\.`) is crucial; without it, `.` is a "wildcard" that matches *any* character. Here, you're looking for the literal dot.
  * `(.*?)`: This is a **non-greedy capturing group**.
      * `.`: The "wildcard" character. It matches any character *except* a newline.
      * `*`: A quantifier meaning "match zero or more of the preceding token."
      * `?`: This makes the `*` quantifier **non-greedy**. A "greedy" `.*` would try to match as much as possible. A "non-greedy" `.*?` matches as *little* as possible while still allowing the rest of the pattern to match.
  * `\n\.A`: This matches a newline character, followed by a literal dot, followed by the literal character `A`.
  * `re.S` (or `re.DOTALL`): This is a **flag** that modifies the behavior of the `.` wildcard. With this flag, `.` **will also match newline characters**. This is essential here because a title or abstract can span multiple lines.

**In short: This regex captures all text that is located between a `.T\n` marker and the *next* `\n.A` marker. This is clearly intended to extract the title section.**

-----

### 3\. Author Match

```python
author_match = re.search(r'\.A\n(.*?)\n\.B', doc_text, re.S)
```

This follows the exact same logic as the title match, but it looks for the text between the **Author** (`.A\n`) and **Bibliography** (`\n.B`) markers.

**In short: This captures the author section.**

-----

### 4\. Bibliography Match

```python
bib_match = re.search(r'\.B\n(.*?)\n\.W', doc_text, re.S)
```

Again, same logic. This finds the text between the **Bibliography** (`.B\n`) and **Words/Text** (`\n.W`) markers.

**In short: This captures the bibliography section.**

-----

### 5\. Text/Words Match

```python
text_match = re.search(r'\.W\n(.*?)$', doc_text, re.S)
```

This one is slightly different.

  * `\.W\n`: Matches the **Words/Text** marker (`.W` followed by a newline).
  * `(.*?)`: The same non-greedy capturing group to get all the content. The `re.S` flag allows it to span multiple lines.
  * `$`: This is an "anchor." It asserts that the pattern must match at the **end of the string**.

**In short: This captures all text from the `.W\n` marker all the way to the very end of the `doc_text` string. This is designed to extract the main body/abstract of the document.**





Packages Used:

Flask,"Your web server; creates the API (e.g., /search, /doc) that the frontend calls."
Flask-CORS,Allows your React frontend (on a different port) to send requests to your Flask server.
scikit-learn,Core search logic. Provides TfidfVectorizer to build the index and cosine_similarity to rank results.
spaCy,"Core NLP. Used for text preprocessing, specifically lemmatization (e.g., ""running"" → ""run"")."
NLTK,"A supporting NLP library used to get the list of English stopwords (e.g., ""the"", ""a"", ""is"")."
SciPy,"Used to efficiently save (save_npz) and load (load_npz) the large, sparse TF-IDF matrix."
NumPy,Performs the high-speed math operations on the vectors and matrices for scikit-learn and scipy.
pandas,Used in the preprocessing script (1_parse...) to easily manage the documents and apply the preprocess function.