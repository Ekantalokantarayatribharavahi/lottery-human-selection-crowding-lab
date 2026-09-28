from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True)
class Feature:
    name: str
    value: float
    label: str
    evidence_basis: str
    rationale: str

FEATURE_ORDER=(
    "date_density","repeat_digit_score","consecutive_score","sequence_score",
    "visual_pattern_score","low_range_density","symmetry_score","human_salience_score",
)

def _validate(combination:list[int])->list[int]:
    if not combination: raise ValueError("combination must not be empty")
    if len(combination)!=len(set(combination)): raise ValueError("combination contains duplicates")
    if any(n<1 or n>52 for n in combination): raise ValueError("numbers must be between 1 and 52")
    return sorted(combination)

def _runs(nums:list[int])->int:
    longest=1
    current=1
    for a,b in zip(nums,nums[1:]):
        if b==a+1:
            current+=1
            longest=max(longest,current)
        else: current=1
    return longest

def extract_features(combination:list[int])->dict[str,Feature]:
    nums=_validate(combination)
    date_count=sum(n<=31 for n in nums)
    digit_counts=Counter(str(n) for n in nums)
    repeated_digits=sum(max(0,c-1) for c in digit_counts.values())
    consecutive_pairs=sum(b==a+1 for a,b in zip(nums,nums[1:]))
    longest_run=_runs(nums)
    differences=[b-a for a,b in zip(nums,nums[1:])]
    arithmetic=len(differences)>=2 and len(set(differences))==1
    low_density=date_count/len(nums)
    symmetric=all((nums[i]+nums[-i-1])==(nums[0]+nums[-1]) for i in range(len(nums)//2))
    parity=(sum(n%2 for n in nums)/len(nums))
    visual=1.0 if (arithmetic or len(set(differences))<=2 and max(differences,default=0)<=10) else 0.0
    salience=min(1.0,0.6*low_density+0.4*(sum(n in {7,8,11,13,18,21,23,24,27,28,31} for n in nums)/len(nums)))
    return {
      "date_density":Feature("date_density",low_density,"HIGH" if low_density>=.67 else "MEDIUM" if low_density>=.34 else "LOW","reasoned proxy","Fraction of values within 1..31, a birthday/date concentration proxy."),
      "repeat_digit_score":Feature("repeat_digit_score",min(1.0,repeated_digits/max(1,len(nums)-1)),"HIGH" if repeated_digits>=2 else "MEDIUM" if repeated_digits==1 else "LOW","reasoned proxy","Measures repeated number-string values at the tens/unit-string level."),
      "consecutive_score":Feature("consecutive_score",min(1.0,consecutive_pairs/max(1,len(nums)-1)),"HIGH" if consecutive_pairs>=2 else "MEDIUM" if consecutive_pairs==1 else "LOW","reasoned proxy","Fraction of adjacent pairs that are consecutive integers."),
      "sequence_score":Feature("sequence_score",1.0 if arithmetic else 0.0,"HIGH" if arithmetic else "LOW","reasoned proxy","Flags exact arithmetic spacing across the sorted combination."),
      "visual_pattern_score":Feature("visual_pattern_score",visual,"HIGH" if visual else "LOW","reasoned proxy","Coarse proxy for simple visible spacing/pattern regularity; no slip geometry inference is used."),
      "low_range_density":Feature("low_range_density",low_density,"HIGH" if low_density>=.67 else "MEDIUM" if low_density>=.34 else "LOW","reasoned proxy","Fraction of values in the low 1..31 range."),
      "symmetry_score":Feature("symmetry_score",1.0 if symmetric else 0.0,"HIGH" if symmetric else "LOW","reasoned proxy","Checks reflection symmetry around a common endpoint sum."),
      "human_salience_score":Feature("human_salience_score",salience,"HIGH" if salience>=.67 else "MEDIUM" if salience>=.34 else "LOW","reasoned proxy","Proxy combining date concentration and a small registered salient-number set."),
    }
