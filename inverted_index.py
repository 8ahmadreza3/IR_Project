from collections import defaultdict


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)  # term -> set of docIDs
        self.vocabulary = set()
    
    def build(self, processed_docs):
        """
        Build inverted index from processed documents
        
        Args:
            processed_docs: dict of {docID: [tokens]}
        """
        for doc_id, tokens in processed_docs.items():
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.index[token].add(doc_id)
                self.vocabulary.add(token)
        
        print(f"Inverted index built with {len(self.index)} terms")
        return self.index
    
    def search(self, query_terms):
        """
        Search for documents containing all query terms (AND query)
        
        Args:
            query_terms: list of tokens
            
        Returns:
            set of docIDs
        """
        if not query_terms:
            return set()
        
        # Start with the first term
        result = set(self.index[query_terms[0]])
        
        # Intersect with other terms
        for term in query_terms[1:]:
            result = result.intersection(self.index[term])
        
        return result
    
    def search_or(self, query_terms):
        """
        Search for documents containing any query term (OR query)
        
        Args:
            query_terms: list of tokens
            
        Returns:
            set of docIDs
        """
        result = set()
        for term in query_terms:
            result = result.union(self.index[term])
        return result
    
    def get_posting_list(self, term):
        """Get posting list for a specific term"""
        return self.index.get(term, set())
    
    def get_vocabulary_size(self):
        """Get vocabulary size"""
        return len(self.vocabulary)
    
    def save_to_file(self, output_file):
        """Save inverted index to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for term in sorted(self.index.keys()):
                    doc_ids = sorted(self.index[term])
                    f.write(f"{term}\t{','.join(doc_ids)}\n")
            print(f"Inverted index saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving inverted index: {e}")
            return False
    
    def load_from_file(self, input_file):
        """Load inverted index from file"""
        try:
            self.index.clear()
            self.vocabulary.clear()
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        term = parts[0]
                        doc_ids = set(parts[1].split(','))
                        self.index[term] = doc_ids
                        self.vocabulary.add(term)
            print(f"Inverted index loaded from {input_file}")
            return True
        except Exception as e:
            print(f"Error loading inverted index: {e}")
            return False
