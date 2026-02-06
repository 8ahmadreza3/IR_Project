# Information Retrieval System - Project Documentation

## Project Overview

This is a complete implementation of an Information Retrieval System for the IR course project. The system is designed to:

1. **Preprocess** text documents (lowercase, remove punctuation, tokenize, stem)
2. **Build indexes** (dictionary and inverted index)
3. **Compress indexes** using gap encoding
4. **Implement Vector Space Model** (TF-IDF + Cosine Similarity)
5. **Search** documents using VSM
6. **Expand queries** with synonyms
7. **Evaluate** system performance with Precision@k

## System Architecture

```
main.py (Entry Point)
    ↓
search_system.py (Main System Orchestrator)
    ├── preprocessing.py (Documents → Tokens & Dictionary)
    ├── inverted_index.py (Term → Documents Mapping)
    ├── compression.py (Gap Encoding Index Compression)
    ├── vector_space_model.py (TF-IDF & Cosine Similarity)
    ├── query_expansion.py (Synonym-based Query Expansion)
    └── evaluation.py (Precision@k Evaluation)
```

## Module Descriptions

### 1. preprocessing.py

**Purpose**: Data preprocessing and dictionary creation

**Key Functions**:

- `lowercase()` - Convert text to lowercase
- `remove_punctuation()` - Remove special characters
- `tokenize()` - Split text into words
- `stem()` - Apply Porter Stemmer (optional)
- `load_documents()` - Load all documents from folder
- `build_dictionary()` - Create term → df mapping
- `save_dictionary()` - Save dictionary to file

**Output**:

- Processed documents (list of tokens)
- Dictionary (term → document frequency)

### 2. inverted_index.py

**Purpose**: Create and manage inverted index

**Key Functions**:

- `build()` - Build inverted index from processed docs
- `search()` - AND query (intersection of posting lists)
- `search_or()` - OR query (union of posting lists)
- `get_posting_list()` - Get documents for a specific term
- `save_to_file()` - Persist inverted index
- `load_from_file()` - Load from disk

**Output**:

- Inverted index (term → set of docIDs)

### 3. compression.py

**Purpose**: Index compression using Gap Encoding

**Key Functions**:

- `gap_encode()` - Compress docID list using gaps
- `gap_decode()` - Decompress docID list
- `compress_index()` - Compress entire index
- `decompress_index()` - Decompress entire index
- `get_compression_ratio()` - Calculate compression percentage

**Method**: Gap Encoding

- Example: DocIDs [1, 3, 5, 7] → gaps [1, 2, 2, 2]

**Output**:

- Compressed index (term → gap list)

### 4. vector_space_model.py

**Purpose**: Vector Space Model with TF-IDF and Cosine Similarity

**Key Functions**:

- `calculate_tf()` - Calculate term frequency
- `calculate_idf()` - Calculate inverse document frequency
- `calculate_tfidf()` - Calculate TF-IDF vectors
- `get_query_vector()` - Convert query to TF-IDF vector
- `cosine_similarity()` - Calculate similarity between query and document
- `rank_documents()` - Rank documents by relevance

**Formulas**:

```
TF(term, doc) = count / doc_length
IDF(term) = log(N / df)
TF-IDF = TF × IDF
Cosine Similarity = (dot product) / (||query|| × ||document||)
```

**Output**:

- Ranked list of documents with similarity scores

### 5. query_expansion.py

**Purpose**: Query expansion using synonyms

**Methods**:

1. **Synonym-based Expansion**: Add synonyms of query terms
2. **Term Weighting**: Boost important query terms

**Key Functions**:

- `expand_with_synonyms()` - Add synonym terms to query
- `set_term_weights()` - Set weight multipliers
- `expand_with_weights()` - Boost term weights
- `create_default_synonyms()` - Create built-in synonym set

**Output**:

- Expanded query terms
- Weighted query vectors

### 6. search_system.py

**Purpose**: Main system orchestration

**Key Functions**:

- `initialize()` - Initialize all system components
- `search()` - Execute search with optional expansion
- `display_results()` - Show results in formatted way
- `save_results()` - Save results to file
- `save_all_models()` - Persist all models and indices

**Workflow**:

1. Load documents → preprocess → build dictionary
2. Build inverted index
3. Compress index
4. Calculate TF-IDF
5. Setup query expansion

### 7. evaluation.py

**Purpose**: System evaluation and performance metrics

**Key Functions**:

- `add_query()` - Add test query with relevant documents
- `add_result()` - Add search results for evaluation
- `calculate_precision_at_k()` - Calculate Precision@k metric
- `evaluate_all_queries()` - Evaluate all test queries
- `print_evaluation_report()` - Display detailed report
- `calculate_average_precision()` - Calculate mean precision

**Metrics**:

```
Precision@k = (relevant_docs_in_top_k) / k
```

## Installation & Setup

### Prerequisites

```bash
Python 3.7+
```

### Optional Dependencies

```bash
pip install nltk numpy
```

### Project Structure

```
IR_Project/
├── main.py                    # Entry point
├── preprocessing.py           # Data preprocessing
├── inverted_index.py          # Inverted index
├── compression.py             # Index compression
├── vector_space_model.py      # VSM & ranking
├── query_expansion.py         # Query expansion
├── search_system.py           # Main system
├── evaluation.py              # Evaluation metrics
└── Documents/                 # Text documents folder
    ├── Doc1.txt
    ├── Doc2.txt
    └── ...
```

## Usage Guide

### Running the System

```bash
python main.py
```

The system will display an interactive menu:

```
============================================================
INFORMATION RETRIEVAL SYSTEM - MENU
============================================================
1. Initialize System (Preprocessing + Indexing)
2. Search with Vector Space Model
3. Search with Query Expansion
4. Evaluate System (Precision@k)
5. Compare Results (With/Without Expansion)
6. Save Models and Indices
7. Exit
============================================================
```

### Menu Options

**Option 1: Initialize System**

- Loads all documents from the Documents folder
- Preprocesses documents (lowercase, remove punctuation, tokenize, stem)
- Builds dictionary (term → df)
- Creates inverted index
- Compresses index using gap encoding
- Calculates TF-IDF vectors
- Sets up query expansion

**Option 2: Standard Search**

- Enter a search query
- System returns top-10 ranked documents
- Option to save results to file

**Option 3: Search with Query Expansion**

- Enter a query
- System automatically expands query with synonyms
- Returns top-10 ranked documents
- Results may differ from standard search

**Option 4: Evaluate System**

- Runs 3 pre-defined test queries
- Test queries: "weather and temperature", "outdoor activities beach", "snow winter cold"
- Pre-defined relevant documents for each query
- Calculates Precision@5 and Precision@10
- Displays detailed evaluation report

**Option 5: Compare Results**

- Enter a query
- Shows top-5 results with and without expansion
- Highlights differences in results

**Option 6: Save Models**

- Saves all models and indices to output directory:
  - `dictionary.txt` - Term to document frequency
  - `inverted_index.txt` - Term to document mapping
  - `compressed_index.txt` - Compressed inverted index
  - `tfidf.txt` - TF-IDF values
  - `synonyms.txt` - Synonym mappings

## Example Queries

Try these sample queries:

1. "weather temperature"
   - Should find documents about weather and temperature

2. "beach activities"
   - Should find documents about beach and outdoor activities

3. "snow cold winter"
   - Should find documents about winter weather

4. "meteorologist predict"
   - Should find documents about weather forecasting

## Output Files

When you save models and results, the following files are created:

```
output/
├── dictionary.txt           # Vocabulary with document frequencies
├── inverted_index.txt       # Inverted index
├── compressed_index.txt     # Compressed index (gap-encoded)
├── tfidf.txt                # TF-IDF vectors
└── synonyms.txt             # Synonym mappings

search_results.txt            # Last search results
evaluation_report.txt         # Evaluation metrics
```

## Implementation Details

### Preprocessing Pipeline

1. Convert to lowercase
2. Remove punctuation and non-alphabetic characters
3. Tokenize (split by whitespace)
4. Remove empty tokens
5. Apply stemming (using Porter Stemmer)

### Index Compression

Uses Gap Encoding:

- DocID list: [Doc1, Doc3, Doc5, Doc7]
- Numeric: [1, 3, 5, 7]
- Gaps: [1, 2, 2, 2]
- Achieves ~30-40% compression for typical document collections

### TF-IDF Calculation

- **TF**: count / document_length (normalized)
- **IDF**: log(N / df) where N = total documents
- **TF-IDF**: TF × IDF

### Query Expansion Methods

1. **Synonym Expansion**: Adds predefined synonyms to query
2. **Term Weighting**: Boosts certain terms with multipliers

### Evaluation Metrics

- **Precision@k**: Fraction of top-k results that are relevant
- **Mean Average Precision@k**: Average precision across multiple queries

## Performance Characteristics

- **Time Complexity**:
  - Indexing: O(N × D) where N=docs, D=avg doc length
  - Search: O(V + R) where V=vocab size, R=result size
  - Ranking: O(N × T) where N=docs, T=query terms

- **Space Complexity**:
  - Dictionary: O(V) where V=vocabulary size
  - Inverted Index: O(V × P) where P=avg posting list length
  - Compression: ~30-40% reduction in index size

## Notes & Limitations

1. **No Positional Index**: Current implementation doesn't support phrase queries
2. **No Stemming Options**: Only Porter Stemmer is implemented
3. **No Phrase Queries**: Only bag-of-words queries
4. **No Field Indexing**: Entire document treated as single field
5. **In-Memory Processing**: Not optimized for very large collections

## Future Enhancements

Possible improvements:

1. Implement positional indexing for phrase queries
2. Add BM25 ranking model
3. Support field-specific queries
4. Implement more compression techniques (Huffman, VarInt)
5. Add relevance feedback mechanism
6. Support boolean queries (AND, OR, NOT)
7. Implement Rocchio's algorithm for query expansion

## References

- Information Retrieval Course Materials
- Manning, Raghavan, Schütze: "Introduction to Information Retrieval"
- Stanford IR Course: https://nlp.stanford.edu/IR-book/

## Author Notes

This system is designed as an educational implementation to demonstrate core IR concepts. It's not optimized for production use with large-scale document collections.

---

**Project Completion Date**: February 2026
