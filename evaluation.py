import os


class SystemEvaluation:
    def __init__(self):
        """Initialize evaluation module"""
        self.queries = {}  # query_id -> query_text
        self.relevant_docs = {}  # query_id -> set of relevant docIDs
        self.results = {}  # query_id -> list of (docID, score) tuples
        self.evaluation_results = {}  # query_id -> {k: precision_at_k}
    
    def add_query(self, query_id, query_text, relevant_docs):
        """
        Add a test query with relevant documents
        
        Args:
            query_id: unique query identifier
            query_text: query string
            relevant_docs: list/set of relevant document IDs
        """
        self.queries[query_id] = query_text
        self.relevant_docs[query_id] = set(relevant_docs)
    
    def add_result(self, query_id, results):
        """
        Add search results for a query
        
        Args:
            query_id: query identifier
            results: list of (docID, score) tuples
        """
        self.results[query_id] = results
    
    def calculate_precision_at_k(self, query_id, k):
        """
        Calculate Precision@k for a query
        
        Args:
            query_id: query identifier
            k: cutoff value
            
        Returns:
            precision value (0 to 1)
        """
        if query_id not in self.results or query_id not in self.relevant_docs:
            return 0.0
        
        results = self.results[query_id]
        relevant = self.relevant_docs[query_id]
        
        # Get top-k results
        top_k = results[:k] if len(results) >= k else results
        
        # Count relevant documents in top-k
        relevant_count = 0
        for doc_id, _ in top_k:
            if doc_id in relevant:
                relevant_count += 1
        
        # Calculate precision
        precision = relevant_count / k if k > 0 else 0
        return precision
    
    def evaluate_all_queries(self, k_values=[5, 10]):
        """
        Evaluate all queries at different k values
        
        Args:
            k_values: list of k values to evaluate
            
        Returns:
            dict of evaluation results
        """
        for query_id in self.queries.keys():
            self.evaluation_results[query_id] = {}
            
            for k in k_values:
                precision = self.calculate_precision_at_k(query_id, k)
                self.evaluation_results[query_id][k] = precision
        
        return self.evaluation_results
    
    def print_evaluation_report(self, k_values=[5, 10]):
        """Print evaluation report"""
        print("\n" + "=" * 60)
        print("SYSTEM EVALUATION REPORT")
        print("=" * 60)
        
        if not self.evaluation_results:
            print("No evaluation results. Run evaluate_all_queries() first.")
            return
        
        for query_id in sorted(self.queries.keys()):
            print(f"\n[Query {query_id}] {self.queries[query_id]}")
            print(f"Relevant documents: {self.relevant_docs[query_id]}")
            
            if query_id in self.results:
                print(f"Retrieved documents (top-10):")
                for rank, (doc_id, score) in enumerate(self.results[query_id][:10], 1):
                    is_relevant = "✓" if doc_id in self.relevant_docs[query_id] else "✗"
                    print(f"  {rank:2d}. {doc_id:8s} {score:.6f} {is_relevant}")
            
            if query_id in self.evaluation_results:
                print(f"Precision values:")
                for k in sorted(self.evaluation_results[query_id].keys()):
                    precision = self.evaluation_results[query_id][k]
                    print(f"  Precision@{k:2d}: {precision:.4f}")
    
    def save_evaluation_report(self, output_file):
        """Save evaluation report to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("SYSTEM EVALUATION REPORT\n")
                f.write("=" * 60 + "\n")
                
                for query_id in sorted(self.queries.keys()):
                    f.write(f"\n[Query {query_id}] {self.queries[query_id]}\n")
                    f.write(f"Relevant documents: {self.relevant_docs[query_id]}\n")
                    
                    if query_id in self.results:
                        f.write(f"Retrieved documents (top-10):\n")
                        for rank, (doc_id, score) in enumerate(self.results[query_id][:10], 1):
                            is_relevant = "YES" if doc_id in self.relevant_docs[query_id] else "NO"
                            f.write(f"  {rank:2d}. {doc_id:8s} {score:.6f} {is_relevant}\n")
                    
                    if query_id in self.evaluation_results:
                        f.write(f"Precision values:\n")
                        for k in sorted(self.evaluation_results[query_id].keys()):
                            precision = self.evaluation_results[query_id][k]
                            f.write(f"  Precision@{k:2d}: {precision:.4f}\n")
            
            print(f"Evaluation report saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving evaluation report: {e}")
            return False
    
    def calculate_average_precision(self, k):
        """
        Calculate Mean Average Precision for all queries at k
        
        Args:
            k: cutoff value
            
        Returns:
            average precision across all queries
        """
        if not self.evaluation_results:
            return 0.0
        
        total = 0
        count = 0
        
        for query_id in self.evaluation_results:
            if k in self.evaluation_results[query_id]:
                total += self.evaluation_results[query_id][k]
                count += 1
        
        return total / count if count > 0 else 0.0
