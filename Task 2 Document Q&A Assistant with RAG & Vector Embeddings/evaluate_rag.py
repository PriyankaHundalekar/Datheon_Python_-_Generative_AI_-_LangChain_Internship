# evaluate_rag.py
from rag_assitant import query_rag_assistant

# Golden Test Dataset: Questions with their expected answers and policy sources
GOLDEN_TEST_DATASET = [
    {
        "id": 1,
        "question": "What is the annual leave limit for permanent staff before days are lost?",
        "expected_keywords": ["1.5", "one and one-half", "statutory entitlement"],
        "source": "Section 6.4 (Annual Leave)"
    },
    {
        "id": 2,
        "question": "Can I use social messaging software or instant messaging during business hours?",
        "expected_keywords": ["not permitted", "instant messaging", "social media"],
        "source": "Section 5.3 (Electronic Communications)"
    },
    {
        "id": 3,
        "question": "What are the minimum hardware processor specifications required for a personal notebook?",
        "expected_keywords": ["Core i5", "Atom", "Celeron", "Pentium"],
        "source": "Section 9.2 (Personal Notebooks)"
    },
    {
        "id": 4,
        "question": "What is the dress code required for men in the office?",
        "expected_keywords": ["Business Casual", "tailored pants", "open neck shirts"],
        "source": "Section 9.9 (Dress Code)"
    },
    {
        "id": 5,
        "question": "What is the capital city of France?", # Out-of-bounds test case for hallucination check
        "expected_keywords": ["I cannot find the answer"],
        "source": "Edge Case / Out-of-Bounds"
    }
]

def run_evaluation():
    print("=" * 60)
    print("🚀 Starting RAG Evaluation Suite for Company Policy Manual")
    print("=" * 60 + "\n")

    passed_tests = 0
    total_tests = len(GOLDEN_TEST_DATASET)

    for test in GOLDEN_TEST_DATASET:
        test_id = test["id"]
        question = test["question"]
        expected_keywords = test["expected_keywords"]
        source_ref = test["source"]

        print(f"Test Case #{test_id}")
        print(f"Question : {question}")
        print(f"Target   : {source_ref}")
        
        # Call your RAG chatbot function
        generated_answer = query_rag_assistant(question)
        print(f"Answer   :\n{generated_answer}\n")

        # Evaluate if at least one expected keyword is present in the response
        match_found = any(keyword.lower() in generated_answer.lower() for keyword in expected_keywords)

        if match_found:
            print(f"Status   : ✅ PASSED\n")
            passed_tests += 1
        else:
            print(f"Status   : ❌ FAILED (Expected keywords {expected_keywords} not found)\n")
        
        print("-" * 60)

    print(f"\nEvaluation Complete: {passed_tests}/{total_tests} test cases passed successfully!")

if __name__ == "__main__":
    run_evaluation()