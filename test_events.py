import json
from audit_ledger import CryptographicAuditLedger
from audit_engine import AuditEngine

def run_demo_events():
    print("=" * 70)
    print("       AUDITCHAIN-AI: RUNNING DEMO EVENTS (A through E)")
    print("=" * 70)

    ledger = CryptographicAuditLedger()
    engine = AuditEngine(ledger=ledger)

    events = [
        {
            "id": "REQ-1001",
            "action": "Purchase $1,200 Monthly SaaS Analytics License",
            "amount": 1200,
            "role": "Software Engineer",
            "date": "2026-09-10"
        },
        {
            "id": "REQ-1002",
            "action": "Execute $8,500 AWS Server Charge for Q3 Infrastructure Expansion",
            "amount": 8500,
            "role": "DevOps Lead",
            "date": "2026-09-15"
        },
        {
            "id": "REQ-1003",
            "action": "Execute $8,500 AWS Server Charge for Q4 Overrun",
            "amount": 8500,
            "role": "DevOps Lead",
            "date": "2026-10-02"
        },
        {
            "id": "REQ-1004",
            "action": "Approve $4,000 Marketing Ad Spend (Approved on Slack by Sarah)",
            "amount": 4000,
            "role": "Marketing Lead",
            "date": "2026-09-20"
        },
        {
            "id": "REQ-1005",
            "action": "Execute $6,000 Server Hardware Overhaul",
            "amount": 6000,
            "role": "IT Director",
            "date": "2026-09-25"
        }
    ]

    for idx, ev in enumerate(events, 1):
        res = engine.evaluate_request(
            request_id=ev["id"],
            action=ev["action"],
            amount=ev["amount"],
            user_role=ev["role"],
            transaction_date=ev["date"]
        )
        
        status_icon = "🟢" if res["decision"] == "APPROVED" else ("🔴" if res["decision"] == "FLAGGED" else "🟠")
        print(f"\n[EVENT {chr(64 + idx)}] {ev['id']} | Date: {ev['date']}")
        print(f"Action: {ev['action']}")
        print(f"Result: {status_icon} {res['decision']}")
        print(f"Rationale: {res['justification']}")
        print(f"Memory Ref: {res['hindsight_memory_id']} | Policy: {res['policy_version']}")
        print("-" * 70)

    is_valid, msg = ledger.verify_integrity()
    print(f"\n🔐 Ledger Integrity Check: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    print(f"Details: {msg}")

    export_data = {
        "ledger_id": "AUDITCHAIN-MAINNET-DEMO",
        "public_key_hex": ledger.get_public_key_hex(),
        "records": ledger.chain
    }

    with open("audit_ledger.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)

    print("\n💾 Saved cryptographic audit ledger to 'audit_ledger.json'.")

if __name__ == "__main__":
    run_demo_events()