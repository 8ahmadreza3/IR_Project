from preprocessing import PreProcessor
from inverted_index import InvertedIndex
from vector_space_model import VectorSpaceModel
from query_expansion import QueryExpansion
from compression import IndexCompression


class SearchSystem:
    def __init__(self, docs_folder, use_stemming=True, use_compression=True):
        """
        Initialize complete search system
        
        Args:
            docs_folder: path to documents folder
            use_stemming: whether to use stemming
            use_compression: whether to use index compression
        """
        self.docs_folder = docs_folder
        self.use_stemming = use_stemming
        self.use_compression = use_compression
        
        # Components
        self.preprocessor = None
        self.inverted_index = None
        self.compressed_index = None
        self.vector_space_model = None
        self.query_expansion = None
        
        self.is_initialized = False
    
    def initialize(self):
        """Initialize all components of the search system"""
        print("=" * 60)
        print("INITIALIZING INFORMATION RETRIEVAL SYSTEM")
        print("=" * 60)
        
        # Step 1: Preprocessing
        print("\n[STEP 1] Data Preprocessing and Dictionary Building")
        print("-" * 60)
        self.preprocessor = PreProcessor(use_stemming=self.use_stemming)
        
        if not self.preprocessor.load_documents(self.docs_folder):
            print("Failed to load documents!")
            return False
        
        if not self.preprocessor.build_dictionary():
            print("Failed to build dictionary!")
            return False
        
        stats = self.preprocessor.get_statistics()
        print(f"\nPreprocessing Statistics:")
        print(f"  - Documents: {stats['num_documents']}")
        print(f"  - Unique Terms: {stats['num_unique_terms']}")
        print(f"  - Total Tokens: {stats['total_tokens']}")
        print(f"  - Avg Tokens per Document: {stats['avg_tokens_per_doc']:.2f}")
        
        # Step 2: Build Inverted Index
        print("\n[STEP 2] Building Inverted Index")
        print("-" * 60)
        self.inverted_index = InvertedIndex()
        self.inverted_index.build(self.preprocessor.processed_docs)
        
        print(f"Inverted index with {self.inverted_index.get_vocabulary_size()} terms")
        
        # Step 3: Compression
        if self.use_compression:
            print("\n[STEP 3] Index Compression (Gap Encoding)")
            print("-" * 60)
            self.compressed_index = IndexCompression.compress_index(self.inverted_index.index)
            
            # Calculate compression ratio
            ratio = IndexCompression.get_compression_ratio(
                self.inverted_index.index,
                self.compressed_index
            )
            print(f"Compression ratio: {ratio:.2f}%")
        
        # Step 4: Vector Space Model
        print("\n[STEP 4] Vector Space Model (TF-IDF)")
        print("-" * 60)
        self.vector_space_model = VectorSpaceModel(
            self.preprocessor,
            stats['num_documents']
        )
        self.vector_space_model.calculate_tf()
        self.vector_space_model.calculate_idf()
        self.vector_space_model.calculate_tfidf()
        print("TF-IDF vectors calculated")
        
        # Step 5: Query Expansion
        print("\n[STEP 5] Query Expansion Setup")
        print("-" * 60)
        self.query_expansion = QueryExpansion()
        self.query_expansion.create_default_synonyms()
        print(f"Query expansion with {len(self.query_expansion.synonyms)} synonym sets")
        
        self.is_initialized = True
        
        print("\n" + "=" * 60)
        print("SYSTEM INITIALIZATION COMPLETE")
        print("=" * 60)
        return True
    
    def search(self, query_text, k=10, use_expansion=False):
        """
        Search for documents matching query
        
        Args:
            query_text: query string
            k: number of top results to return
            use_expansion: whether to use query expansion
            
        Returns:
            list of (docID, similarity_score) tuples
        """
        if not self.is_initialized:
            print("Error: System not initialized!")
            return []
        
        # Preprocess query
        query_tokens = self.preprocessor.preprocess_text(query_text)
        
        if not query_tokens:
            print("Empty query after preprocessing")
            return []
        
        print(f"\nQuery (original): {query_text}")
        print(f"Query (processed): {query_tokens}")
        
        # Get query vector
        query_vector = self.vector_space_model.get_query_vector(query_tokens)
        
        # Expand query if requested
        if use_expansion:
            expanded_tokens = self.query_expansion.expand_with_synonyms(query_tokens)
            query_vector = self.vector_space_model.get_query_vector(expanded_tokens)
            print(f"Query (expanded): {expanded_tokens}")
        
        # Rank documents
        results = self.vector_space_model.rank_documents(query_vector, k=k)
        
        return results
    
    def display_results(self, results, show_content=False, content_preview_len=200):
        """
        Display search results
        
        Args:
            results: list of (docID, similarity_score) tuples
            show_content: whether to show document content
            content_preview_len: length of content preview
        """
        print("\n" + "=" * 60)
        print("SEARCH RESULTS")
        print("=" * 60)
        
        if not results:
            print("No documents found.")
            return
        
        for rank, (doc_id, score) in enumerate(results, 1):
            print(f"\n[{rank}] {doc_id}  (Score: {score:.6f})")
            
            if show_content and doc_id in self.preprocessor.documents:
                content = self.preprocessor.documents[doc_id]
                preview = content[:content_preview_len] + "..." if len(content) > content_preview_len else content
                print(f"    Preview: {preview}")
    
    def save_results(self, results, output_file):
        """Save search results to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for rank, (doc_id, score) in enumerate(results, 1):
                    f.write(f"{rank}\t{doc_id}\t{score:.6f}\n")
            print(f"Results saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False
    
    def save_all_models(self, output_dir="output"):
        """Save all models and indices to files"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save dictionary
        self.preprocessor.save_dictionary(os.path.join(output_dir, "dictionary.txt"))
        
        # Save inverted index
        self.inverted_index.save_to_file(os.path.join(output_dir, "inverted_index.txt"))
        
        # Save compressed index
        if self.use_compression:
            IndexCompression.save_compressed_index(
                self.compressed_index,
                os.path.join(output_dir, "compressed_index.txt")
            )
        
        # Save TF-IDF
        self.vector_space_model.save_tfidf(os.path.join(output_dir, "tfidf.txt"))
        
        # Save synonyms
        self.query_expansion.save_synonyms(os.path.join(output_dir, "synonyms.txt"))
        
        print(f"All models saved to {output_dir}/")
