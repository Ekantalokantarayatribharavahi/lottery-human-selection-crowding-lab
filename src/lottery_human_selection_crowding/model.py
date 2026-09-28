from __future__ import annotations
from dataclasses import dataclass
from .features import Feature

@dataclass(frozen=True)
class Weight:
    feature: str
    value: float
    evidence_basis: str
    rationale: str

DEFAULT_WEIGHTS={
 "date_density":Weight("date_density",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "repeat_digit_score":Weight("repeat_digit_score",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "consecutive_score":Weight("consecutive_score",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "sequence_score":Weight("sequence_score",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "visual_pattern_score":Weight("visual_pattern_score",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "low_range_density":Weight("low_range_density",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "symmetry_score":Weight("symmetry_score",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
 "human_salience_score":Weight("human_salience_score",1.0,"reasoned proxy","Equal baseline proxy weight; replace with empirical evidence when available."),
}

def score_features(features:dict[str,Feature],weights:dict[str,Weight]|None=None)->float:
    weights=weights or DEFAULT_WEIGHTS
    total=sum(weights[k].value*features[k].value for k in features)
    scale=sum(abs(weights[k].value) for k in features)
    return 0.0 if scale==0 else total/scale

def explain(features:dict[str,Feature],weights:dict[str,Weight]|None=None)->list[dict]:
    weights=weights or DEFAULT_WEIGHTS
    return [{"feature":k,"value":features[k].value,"label":features[k].label,"weight":weights[k].value,"contribution":features[k].value*weights[k].value,"evidence_basis":features[k].evidence_basis,"rationale":features[k].rationale} for k in features]
