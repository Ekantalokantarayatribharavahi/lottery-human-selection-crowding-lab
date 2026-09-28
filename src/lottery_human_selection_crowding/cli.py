from __future__ import annotations
import argparse,json
from .features import extract_features
from .model import score_features,explain

MESSAGE="Crowding score estimates expected player-selection concentration; it does not alter the lottery draw probability."

def main()->int:
    p=argparse.ArgumentParser(prog="crowding")
    s=p.add_subparsers(dest="cmd",required=True)
    for name in ("score","explain"):
        q=s.add_parser(name); q.add_argument("--game",required=True,choices=["lotto","powerball","daily_lotto"]); q.add_argument("--combination",required=True)
    a=p.parse_args()
    nums=[int(x.strip()) for x in a.combination.split(",") if x.strip()]
    features=extract_features(nums)
    value=score_features(features)
    payload={"game":a.game,"combination":sorted(nums),"crowding_score":value,"message":MESSAGE,"features":explain(features)}
    if a.cmd=="score": print(json.dumps(payload,sort_keys=True))
    else:
        print(MESSAGE)
        print(f"Combination: {' '.join(map(str,sorted(nums)))}")
        for f in payload["features"]:
            print(f"{f['feature']}: {f['label']} ({f['value']:.3f}) — {f['evidence_basis']}")
        print(f"Explainable score: {value:.6f}")
    return 0

if __name__=="__main__": raise SystemExit(main())
