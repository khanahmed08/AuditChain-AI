import time
import json
from audit_ledger import CryptographicAuditLedger
from audit_engine import AuditEngine

def run_benchmark():
    print("=" * 68)
    print("       AUDITCHAIN-AI: PERFORMANCE & ACCURACY BENCHMARK       ")
    print("=" * 68)

    ledger = CryptographicAuditLedger()
    engine = AuditEngine(ledger=ledger)

    # Synthetic Test Suite: 50 Scenarios
    # Ground Truth: 20 Approved, 20 Flagged, 10 Escalated
    synthetic_cases = []
    
    # 20 Valid Low-Risk / Approved Cases
    for i in range(20):
        synthetic_cases.append({
            "id": f"BENCH-A-{i:02d}",
            "action": f"Purchase ${500 + i*50} Office Equipment Supplies",
            "amount": 500 + i*50,
            "role": "Operations Manager",
            "date": "2026-09-15",
            "expected": "APPROVED"
        })

    # 20 Expired / Un-authorized / Flagged Cases
    for i in range(20):
        synthetic_cases.append({
            "id": f"BENCH-F-{i:02d}",
            "action": f"Execute $8,500 AWS Server Charge for Q4",
            "amount": 8500,
            "role": "DevOps Lead",
            "date": "2026-10-15", # Expired policy
            "expected": "FLAGGED"
        })

    # 10 Contradictory / Escalated Cases
    for i in range(10):
        synthetic_cases.append({
            "id": f"BENCH-E-{i:02d}",
            "action": f"Execute $6,000 Server Hardware Overhaul #{i}",
            "amount": 6000,
            "role": "IT Lead",
            "date": "2026-09-20",
            "expected": "ESCALATED"
        })

    latencies = []
    tp, fp, tn, fn = 0, 0, 0, 0

    print(f"🚀 Processing {len(synthetic_cases)} synthetic governance evaluation scenarios...")
    
    for case in synthetic_cases:
        t0 = time.perf_counter()
        res = engine.evaluate_request(
            request_id=case["id"],
            action=case["action"],
            amount=case["amount"],
            user_role=case["role"],
            transaction_date=case["date"]
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        latencies.append(elapsed_ms)

        actual = res["decision"]
        expected = case["expected"]

        # Metric classification (APPROVED vs NON-APPROVED)
        if expected == "APPROVED" and actual == "APPROVED":
            tp += 1
        elif expected != "APPROVED" and actual == "APPROVED":
            fp += 1
        elif expected != "APPROVED" and actual != "APPROVED":
            tn += 1
        elif expected == "APPROVED" and actual != "APPROVED":
            fn += 1

    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 100.0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 100.0
    accuracy = ((tp + tn) / len(synthetic_cases)) * 100
    p95_latency = sorted(latencies)[int(0.95 * len(latencies))]
    avg_latency = sum(latencies) / len(latencies)

    print("-" * 68)
    print("                     EVALUATION METRICS                       ")
    print("-" * 68)
    print(f"• Total Test Cases Processed : {len(synthetic_cases)}")
    print(f"• Precision                  : {precision:.1f}%")
    print(f"• Recall                     : {recall:.1f}%")
    print(f"• Overall Accuracy           : {accuracy:.1f}%")
    print(f"• Average Latency            : {avg_latency:.2f} ms")
    print(f"• P95 Latency                : {p95_latency:.2f} ms")
    print("-" * 68)
    print("Confusion Matrix:")
    print(f"  True Positives  (TP) : {tp}")
    print(f"  False Positives (FP) : {fp}")
    print(f"  True Negatives  (TN) : {tn}")
    print(f"  False Negatives (FN) : {fn}")
    print("=" * 68)

    # Save benchmark result for Streamlit UI import
    metrics_summary = {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "p95_latency_ms": p95_latency,
        "avg_latency_ms": avg_latency,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn
    }

    with open("benchmark_results.json", "w") as f:
        json.dump(metrics_summary, f, indent=2)

    print("💾 Saved metric benchmarks to 'benchmark_results.json'.")

if __name__ == "__main__":
    run_benchmark()