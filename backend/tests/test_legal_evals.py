import pytest
import json
import os
from app.utils.bns_mapping import validate_citations, BNS_MAPPING

def test_evals_suite_50_queries():
    evals_path = os.path.join(os.path.dirname(__file__), "../evals/legal_queries.json")
    with open(evals_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    assert len(dataset) == 50, f"Expected 50 legal queries, found {len(dataset)}"
    
    hallucination_count = 0
    passed_queries = 0
    
    for item in dataset:
        expected_bns = item.get("expected_bns_statute", "")
        ground_truth = item.get("ground_truth_answer", "")
        
        # Test Citation Validator
        check = validate_citations(ground_truth)
        if not check["compliant_2024"]:
            hallucination_count += 1
        else:
            passed_queries += 1
            
    assert hallucination_count == 0, f"Found {hallucination_count} hallucinated repealed laws!"
    assert passed_queries == 50, "All 50 queries must strictly pass 2024 compliance"
