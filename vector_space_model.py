import math
from collections import defaultdict


class VectorSpaceModel:
    def __init__(self, preprocessor, num_docs):
        """
        Initialize VSM
        
        Args:
            preprocessor: PreProcessor object with processed documents
            num_docs: total number of documents
        """
        self.preprocessor = preprocessor
        self.num_docs = num_docs
        self.tf = {}  # docID -> {term: tf_value}
        self.idf = {}  # term -> idf_value
        self.tfidf = {}  # docID -> {term: tfidf_value}
        self.doc_norms = {}  # docID -> norm of tfidf vector
    
    def calculate_tf(self):
        """Calculate TF (Term Frequency) for each document"""
        for doc_id, tokens in self.preprocessor.processed_docs.items():
            term_counts = defaultdict(int)
            
            for token in tokens:
                term_counts[token] += 1
            
            doc_length = len(tokens)
            self.tf[doc_id] = {}
            
            # TF = count / doc_length (normalized)
            for term, count in term_counts.items():
                self.tf[doc_id][term] = count / doc_length if doc_length > 0 else 0
        
        print(f"TF calculated for {len(self.tf)} documents")
    
    def calculate_idf(self):
        """Calculate IDF (Inverse Document Frequency) for each term"""
        term_doc_count = {}
        
        for doc_id, tokens in self.preprocessor.processed_docs.items():
            unique_terms = set(tokens)
            for term in unique_terms:
                if term not in term_doc_count:
                    term_doc_count[term] = 0
                term_doc_count[term] += 1
        
        # IDF = log(N / df)  where N is total documents, df is document frequency
        for term, doc_count in term_doc_count.items():
            if doc_count > 0:
                self.idf[term] = math.log(self.num_docs / doc_count)
        
        print(f"IDF calculated for {len(self.idf)} terms")
    
    def calculate_tfidf(self):
        """Calculate TF-IDF for all documents"""
        for doc_id in self.tf.keys():
            self.tfidf[doc_id] = {}
            
            for term in self.tf[doc_id].keys():
                tf_value = self.tf[doc_id][term]
                idf_value = self.idf.get(term, 0)
                tfidf_value = tf_value * idf_value
                self.tfidf[doc_id][term] = tfidf_value
        
        # Calculate document norms for cosine similarity
        for doc_id in self.tfidf.keys():
            norm = math.sqrt(sum(v**2 for v in self.tfidf[doc_id].values()))
            self.doc_norms[doc_id] = norm
        
        print(f"TF-IDF calculated for {len(self.tfidf)} documents")
    
    def get_query_vector(self, query_tokens):
        """
        Calculate TF-IDF vector for query
        
        Args:
            query_tokens: list of tokens in query
            
        Returns:
            dict of {term: tfidf_value}
        """
        query_tf = defaultdict(int)
        
        for token in query_tokens:
            query_tf[token] += 1
        
        query_length = len(query_tokens)
        query_vector = {}
        
        for term, count in query_tf.items():
            tf_value = count / query_length if query_length > 0 else 0
            idf_value = self.idf.get(term, 0)
            query_vector[term] = tf_value * idf_value
        
        return query_vector
    
    def cosine_similarity(self, query_vector, doc_id):
        """
        Calculate cosine similarity between query and document
        
        Args:
            query_vector: dict of {term: tfidf_value}
            doc_id: document ID
            
        Returns:
            similarity score (0 to 1)
        """
        if doc_id not in self.tfidf:
            return 0.0
        
        doc_vector = self.tfidf[doc_id]
        
        # Calculate dot product
        dot_product = 0
        for term in query_vector:
            if term in doc_vector:
                dot_product += query_vector[term] * doc_vector[term]
        
        # Calculate query norm
        query_norm = math.sqrt(sum(v**2 for v in query_vector.values()))
        
        # Calculate cosine similarity
        denominator = query_norm * self.doc_norms[doc_id]
        if denominator == 0:
            return 0.0
        
        similarity = dot_product / denominator
        return similarity
    
    def rank_documents(self, query_vector, k=10):
        """
        Rank all documents based on cosine similarity with query
        
        Args:
            query_vector: dict of {term: tfidf_value}
            k: number of top documents to return
            
        Returns:
            list of (docID, similarity_score) tuples, sorted by score
        """
        scores = []
        
        for doc_id in self.tfidf.keys():
            similarity = self.cosine_similarity(query_vector, doc_id)
            if similarity > 0:  # Only include documents with non-zero similarity
                scores.append((doc_id, similarity))
        
        # Sort by similarity score in descending order
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:k]
    
    def save_tfidf(self, output_file):
        """Save TF-IDF values to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for doc_id in sorted(self.tfidf.keys()):
                    f.write(f"{doc_id}\n")
                    terms = sorted(self.tfidf[doc_id].keys())
                    for term in terms:
                        tfidf_val = self.tfidf[doc_id][term]
                        f.write(f"  {term}\t{tfidf_val:.6f}\n")
            print(f"TF-IDF values saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving TF-IDF: {e}")
            return False
