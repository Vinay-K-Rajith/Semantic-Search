"""
Test semantic search with sample queries.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Sample queries for semantic search
SAMPLE_QUERIES = [
    "Learn Python fundamentals and variables",
    "Data structures like lists and dictionaries",
    "Machine learning and regression models",
    "Web development frameworks",
    "Database and SQL queries",
    "Neural networks and deep learning",
    "Cloud deployment on Azure",
    "Object-oriented programming concepts",
    "Text processing with NLP",
    "Computer vision techniques"
]

def test_health():
    """Test health endpoint."""
    print("\n" + "="*60)
    print("Testing health endpoint...")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_subtopics_count():
    """Test subtopics count endpoint."""
    print("\n" + "="*60)
    print("Testing subtopics count...")
    print("="*60)
    response = requests.get(f"{BASE_URL}/subtopics/count")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Indexed subtopics: {data['indexed_subtopics']}")

def test_search(query, top_k=5):
    """Test search endpoint."""
    print("\n" + "-"*60)
    print(f"Query: '{query}'")
    print(f"Top K: {top_k}")
    print("-"*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/search",
            json={"query": query, "top_k": top_k},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Found {data['total']} results in {data['time_ms']}ms")
            print()
            
            for i, result in enumerate(data['results'], 1):
                print(f"  {i}. Video: {result['file_name']}")
                print(f"     Caption: {result['caption']}")
                print(f"     SubTopic: {result['subtopic']}")
                print(f"     Score: {result['score']:.4f}")
                print(f"     Thumbnail: {result['thumbnail']}")
                print()
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SEMANTIC SEARCH TEST SUITE")
    print("="*60)
    
    # Test health
    test_health()
    
    # Test subtopics count
    test_subtopics_count()
    
    # Test semantic search with various queries
    print("\n" + "="*60)
    print("SEMANTIC SEARCH TESTS")
    print("="*60)
    
    for query in SAMPLE_QUERIES:
        test_search(query, top_k=3)
    
    print("\n" + "="*60)
    print("✅ TEST SUITE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
