#!/usr/bin/env python3
"""
Quick Demonstration Script
Shows the entire IR system in action with a few example queries
"""

import os
from search_system import SearchSystem
from evaluation import SystemEvaluation


def main():
    """Run a quick demonstration"""
    docs_folder = "Documents"
    
    print("=" * 70)
    print("INFORMATION RETRIEVAL SYSTEM - QUICK DEMONSTRATION")
    print("=" * 70)
    
    # Initialize system
    print("\n[STEP 1] Initializing the system...")
    search_system = SearchSystem(docs_folder, use_stemming=True, use_compression=True)
    
    if not search_system.initialize():
        print("Failed to initialize system!")
        return
    
    # Demo queries
    demo_queries = [
        ("weather and temperature", False),
        ("beach activities", False),
        ("snow winter", True),  # This one uses expansion
    ]
    
    print("\n" + "=" * 70)
    print("DEMO: SEARCHING WITH SAMPLE QUERIES")
    print("=" * 70)
    
    for i, (query, use_expansion) in enumerate(demo_queries, 1):
        expansion_text = "WITH Query Expansion" if use_expansion else "WITHOUT Query Expansion"
        print(f"\n[DEMO {i}] Searching: '{query}' ({expansion_text})")
        print("-" * 70)
        
        results = search_system.search(query, k=5, use_expansion=use_expansion)
        search_system.display_results(results, show_content=False)
    
    # Evaluation Demo
    print("\n" + "=" * 70)
    print("DEMO: SYSTEM EVALUATION")
    print("=" * 70)
    
    evaluation = SystemEvaluation()
    
    # Add test queries
    evaluation.add_query("Q1", "weather", ["Doc1", "Doc2"])
    evaluation.add_query("Q2", "beach activities outdoor", ["Doc1", "Doc5"])
    evaluation.add_query("Q3", "snow", ["Doc1", "Doc3"])
    
    print("\n[Running Test Queries...]")
    for query_id in ["Q1", "Q2", "Q3"]:
        query_text = evaluation.queries[query_id]
        results = search_system.search(query_text, k=10, use_expansion=False)
        evaluation.add_result(query_id, results)
        print(f"  {query_id}: {query_text:35s} → {len(results)} results")
    
    # Evaluate
    evaluation.evaluate_all_queries(k_values=[5, 10])
    evaluation.print_evaluation_report(k_values=[5, 10])
    
    # Save outputs
    print("\n" + "=" * 70)
    print("SAVING OUTPUTS")
    print("=" * 70)
    
    os.makedirs("output", exist_ok=True)
    
    search_system.save_all_models("output")
    evaluation.save_evaluation_report("output/evaluation_demo.txt")
    
    print("\n✓ Demonstration completed!")
    print("✓ Check the 'output' folder for saved models and reports")
    print("✓ Run 'python main.py' for interactive mode")


if __name__ == "__main__":
    main()
