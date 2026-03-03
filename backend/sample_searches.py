#!/usr/bin/env python
"""
Sample semantic search queries to test the system.
Run with: python sample_searches.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Sample queries for semantic search
SAMPLE_QUERIES = [
    "Python programming basics and setup",
    "Machine learning and data science",
    "Web development frameworks",
    "Database management SQL",
    "Cloud deployment and DevOps",
    "Neural networks and deep learning",
    "Natural language processing techniques",
    "Object-oriented design patterns",
]

def test_health():
    """Test API health."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("[OK] Health Check:")
        print(f"   Status: {response.json()['status']}")
        print(f"   Message: {response.json()['message']}\n")
        return True
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}\n")
        return False

def test_subtopics_count():
    """Get the number of indexed subtopics."""
    try:
        response = requests.get(f"{BASE_URL}/subtopics/count", timeout=5)
        data = response.json()
        print(f"[OK] Indexed Subtopics: {data['indexed_subtopics']}\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to get subtopic count: {e}\n")
        return False

def test_semantic_search(query, top_k=5):
    """Perform a semantic search query."""
    try:
        payload = {
            "query": query,
            "top_k": top_k
        }
        response = requests.post(
            f"{BASE_URL}/search",
            json=payload,
            timeout=15
        )
        data = response.json()
        
        print(f"[QUERY] '{query}'")
        print(f"   Time: {data['time_ms']}ms | Results: {data['total']}")
        
        for i, result in enumerate(data['results'], 1):
            print(f"\n   {i}. Video: {result['caption']}")
            print(f"      SubTopic: {result['subtopic']}")
            print(f"      File: {result['file_name']}")
            print(f"      Score: {result['score']:.4f}")
        
        print("\n" + "="*80 + "\n")
        return True
    except Exception as e:
        print(f"[ERROR] Search failed: {e}\n")
        return False

if __name__ == "__main__":
    print("="*80)
    print("[SEARCH] SEMANTIC SEARCH API - SAMPLE TESTS")
    print("="*80 + "\n")
    
    # Test health
    if not test_health():
        print("[ERROR] API is not running. Start with: python -m uvicorn main:app --reload")
        exit(1)
    
    # Get subtopic count
    test_subtopics_count()
    
    # Run sample searches
    print("[*] Running Sample Semantic Searches...\n")
    print("="*80 + "\n")
    
    for query in SAMPLE_QUERIES:
        test_semantic_search(query, top_k=3)
    
    print("="*80)
    print("[+] All samples completed!")
    print("="*80)
