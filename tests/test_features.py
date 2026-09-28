import pytest
from lottery_human_selection_crowding.features import extract_features
from lottery_human_selection_crowding.model import score_features

def test_feature_extraction_is_deterministic():
    c=[7,18,29,34,41,52]
    assert extract_features(c)==extract_features(c)

def test_low_numbers_raise_date_density():
    a=extract_features([1,2,3,4,5,6])["date_density"].value
    b=extract_features([32,36,40,44,48,52])["date_density"].value
    assert a>b

def test_exact_arithmetic_sequence_is_detected():
    assert extract_features([5,10,15,20,25,30])["sequence_score"].value==1.0

def test_invalid_candidate_rejected():
    with pytest.raises(ValueError):
        extract_features([1,1,2,3,4,5])

def test_identical_candidates_have_identical_scores():
    c=[7,18,29,34,41,52]
    assert score_features(extract_features(c))==score_features(extract_features(c))
