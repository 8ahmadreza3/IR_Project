#!/usr/bin/env python3
"""
Information Retrieval System - Main Entry Point
Complete implementation with all components
"""

import os
import sys
from search_system import SearchSystem
from evaluation import SystemEvaluation


def print_menu():
    """Print main menu"""
    print("\n" + "=" * 60)
    print("INFORMATION RETRIEVAL SYSTEM - MENU")
    print("=" * 60)
    print("1. Initialize System (Preprocessing + Indexing)")
    print("2. Search with Vector Space Model")
    print("3. Search with Query Expansion")
    print("4. Evaluate System (Precision@k)")
    print("5. Compare Results (With/Without Expansion)")
    print("6. Save Models and Indices")
    print("7. Exit")
    print("=" * 60)


def main():
    """Main function"""
    docs_folder = "Documents"
    
    # Check if Documents folder exists
    if not os.path.exists(docs_folder):
        print(f"Error: Documents folder not found at {docs_folder}")
        print("Please ensure the Documents folder exists in the current directory.")
        return
    
    # Initialize search system
    search_system = SearchSystem(docs_folder, use_stemming=True, use_compression=True)
    evaluation = SystemEvaluation()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            # Initialize System
            if not search_system.is_initialized:
                search_system.initialize()
            else:
                print("System already initialized!")
        
        elif choice == "2":
            # Standard Search
            if not search_system.is_initialized:
                print("System not initialized. Please select option 1 first.")
            else:
                query = input("Enter your search query: ").strip()
                if query:
                    results = search_system.search(query, k=10, use_expansion=False)
                    search_system.display_results(results, show_content=False)
                    
                    save_result = input("Save results? (y/n): ").strip().lower()
                    if save_result == 'y':
                        output_file = "search_results.txt"
                        search_system.save_results(results, output_file)
        
        elif choice == "3":
            # Search with Query Expansion
            if not search_system.is_initialized:
                print("System not initialized. Please select option 1 first.")
            else:
                query = input("Enter your search query: ").strip()
                if query:
                    results = search_system.search(query, k=10, use_expansion=True)
                    search_system.display_results(results, show_content=False)
        
        elif choice == "4":
            # Evaluate System
            if not search_system.is_initialized:
                print("System not initialized. Please select option 1 first.")
            else:
                print("\n" + "=" * 60)
                print("SYSTEM EVALUATION")
                print("=" * 60)
                print("Adding test queries and relevant documents...")
                
                # Query 1: Weather
                evaluation.add_query(
                    "Q1",
                    "weather and temperature",
                    ["Doc1", "Doc2", "Doc3"]
                )
                
                # Query 2: Activities
                evaluation.add_query(
                    "Q2",
                    "outdoor activities beach",
                    ["Doc1", "Doc2", "Doc5"]
                )
                
                # Query 3: Seasons
                evaluation.add_query(
                    "Q3",
                    "snow winter cold",
                    ["Doc1", "Doc3", "Doc4"]
                )
                
                # Run searches and collect results
                print("\nRunning queries...")
                for query_id in ["Q1", "Q2", "Q3"]:
                    query_text = evaluation.queries[query_id]
                    results = search_system.search(query_text, k=10, use_expansion=False)
                    evaluation.add_result(query_id, results)
                    print(f"  {query_id}: Found {len(results)} documents")
                
                # Evaluate
                evaluation.evaluate_all_queries(k_values=[5, 10])
                evaluation.print_evaluation_report(k_values=[5, 10])
                
                # Save evaluation report
                save_eval = input("Save evaluation report? (y/n): ").strip().lower()
                if save_eval == 'y':
                    evaluation.save_evaluation_report("evaluation_report.txt")
        
        elif choice == "5":
            # Compare Results
            if not search_system.is_initialized:
                print("System not initialized. Please select option 1 first.")
            else:
                query = input("Enter your search query: ").strip()
                if query:
                    print("\n" + "=" * 60)
                    print("COMPARISON: WITH/WITHOUT QUERY EXPANSION")
                    print("=" * 60)
                    
                    # Without expansion
                    print("\n1. WITHOUT QUERY EXPANSION:")
                    results_without = search_system.search(query, k=5, use_expansion=False)
                    search_system.display_results(results_without, show_content=False)
                    
                    # With expansion
                    print("\n2. WITH QUERY EXPANSION:")
                    results_with = search_system.search(query, k=5, use_expansion=True)
                    search_system.display_results(results_with, show_content=False)
                    
                    # Comparison
                    print("\n" + "-" * 60)
                    print("DIFFERENCES:")
                    without_docs = set(doc for doc, _ in results_without)
                    with_docs = set(doc for doc, _ in results_with)
                    
                    new_docs = with_docs - without_docs
                    if new_docs:
                        print(f"New documents with expansion: {new_docs}")
                    else:
                        print("No new documents with expansion")
        
        elif choice == "6":
            # Save Models
            if not search_system.is_initialized:
                print("System not initialized. Please select option 1 first.")
            else:
                output_dir = input("Enter output directory (default: output): ").strip()
                if not output_dir:
                    output_dir = "output"
                search_system.save_all_models(output_dir)
        
        elif choice == "7":
            print("\nThank you for using Information Retrieval System!")
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
