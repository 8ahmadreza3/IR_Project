import os
import re
from collections import defaultdict
try:
    from nltk.stem import PorterStemmer
    NLTK_AVAILABLE = True
except:
    NLTK_AVAILABLE = False


class PreProcessor:
    def __init__(self, use_stemming=True):
        self.use_stemming = use_stemming and NLTK_AVAILABLE
        if self.use_stemming:
            self.stemmer = PorterStemmer()
        self.documents = {}
        self.dictionary = {}  # term -> df (document frequency)
        self.processed_docs = {}  # docID -> list of tokens
    
    def lowercase(self, text):
        """Convert text to lowercase"""
        return text.lower()
    
    def remove_punctuation(self, text):
        """Remove punctuation and non-alphabetic characters"""
        text = re.sub(r'[^a-z\s]', '', text)
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return text.split()
    
    def stem(self, tokens):
        """Apply stemming to tokens"""
        if self.use_stemming:
            return [self.stemmer.stem(token) for token in tokens]
        return tokens
    
    def preprocess_text(self, text):
        """Apply all preprocessing steps"""
        # Step 1: Lowercase
        text = self.lowercase(text)
        # Step 2: Remove punctuation
        text = self.remove_punctuation(text)
        # Step 3: Tokenize
        tokens = self.tokenize(text)
        # Step 4: Remove empty tokens
        tokens = [t for t in tokens if t.strip()]
        # Step 5: Stemming (optional)
        tokens = self.stem(tokens)
        return tokens
    
    def load_documents(self, docs_folder):
        """Load and preprocess all documents from folder"""
        if not os.path.exists(docs_folder):
            print(f"Error: Documents folder not found at {docs_folder}")
            return False
        
        doc_files = sorted([f for f in os.listdir(docs_folder) if f.endswith('.txt')])
        print(f"Found {len(doc_files)} documents")
        
        for doc_file in doc_files:
            doc_path = os.path.join(docs_folder, doc_file)
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use filename without extension as docID
                doc_id = doc_file.replace('.txt', '')
                
                # Preprocess the document
                tokens = self.preprocess_text(content)
                
                self.documents[doc_id] = content
                self.processed_docs[doc_id] = tokens
                
                print(f"Loaded and processed: {doc_id} ({len(tokens)} tokens)")
            except Exception as e:
                print(f"Error processing {doc_file}: {e}")
                return False
        
        return True
    
    def build_dictionary(self):
        """Build dictionary: term -> df (document frequency)"""
        term_docs = defaultdict(set)  # term -> set of docIDs
        
        for doc_id, tokens in self.processed_docs.items():
            unique_tokens = set(tokens)
            for token in unique_tokens:
                term_docs[token].add(doc_id)
        
        # Convert to term -> df
        self.dictionary = {term: len(docs) for term, docs in term_docs.items()}
        
        print(f"\nDictionary created with {len(self.dictionary)} unique terms")
        return self.dictionary
    
    def save_dictionary(self, output_file):
        """Save dictionary to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for term in sorted(self.dictionary.keys()):
                    f.write(f"{term}\t{self.dictionary[term]}\n")
            print(f"Dictionary saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving dictionary: {e}")
            return False
    
    def get_statistics(self):
        """Get preprocessing statistics"""
        num_docs = len(self.documents)
        num_terms = len(self.dictionary)
        total_tokens = sum(len(tokens) for tokens in self.processed_docs.values())
        avg_tokens = total_tokens / num_docs if num_docs > 0 else 0
        
        stats = {
            'num_documents': num_docs,
            'num_unique_terms': num_terms,
            'total_tokens': total_tokens,
            'avg_tokens_per_doc': avg_tokens,
            'vocabulary_size': num_terms
        }
        return stats
