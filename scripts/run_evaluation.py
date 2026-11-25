import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.data import load_trusted_records, load_cases
from backend.engine import analyze_record

trusted = load_trusted_records()
cases = load_cases()
tp=tn=fp=fn=0
rows=[]
for case in cases:
    result = analyze_record(case["record"], trusted)
    predicted = "CONSISTENT" if result["decision"] == "CONSISTENT_CANDIDATE" else "CONFLICT"
    actual = case["label"]
    if actual == "CONSISTENT" and predicted == "CONSISTENT": tp += 1
    elif actual == "CONFLICT" and predicted == "CONFLICT": tn += 1
    elif actual == "CONFLICT" and predicted == "CONSISTENT": fp += 1
    else: fn += 1
    rows.append((case["case_id"], actual, predicted, result["decision"], result["confidence"]))
precision = tp/(tp+fp) if tp+fp else 0
recall = tp/(tp+fn) if tp+fn else 0
f1 = 2*precision*recall/(precision+recall) if precision+recall else 0
conflict_precision = tn/(tn+fn) if tn+fn else 0
conflict_recall = tn/(tn+fp) if tn+fp else 0
conflict_f1 = (2*conflict_precision*conflict_recall/(conflict_precision+conflict_recall)
               if conflict_precision+conflict_recall else 0)
macro_f1 = (f1 + conflict_f1) / 2
print("Synthetic benchmark results (not production performance)")
print("Case | Actual | Predicted | Decision | Confidence")
for row in rows: print(" | ".join(map(str,row)))
print(f"\nTP={tp} TN={tn} FP={fp} FN={fn}")
print(f"Consistency-class precision={precision:.3f} recall={recall:.3f} F1={f1:.3f}")
print(f"Conflict-class precision={conflict_precision:.3f} recall={conflict_recall:.3f} F1={conflict_f1:.3f}")
print(f"Binary macro F1={macro_f1:.3f}")
print(f"Accuracy={(tp+tn)/len(cases):.3f}")
