import json
import hashlib
import sys
from cryptography.hazmat.primitives.asymmetric import ed25519

def verify_ledger(ledger_path: str = "audit_ledger.json"):
    print("=" * 68)
    print("         INDEPENDENT AUDITOR CLI - VERIFICATION ENGINE         ")
    print("=" * 68)

    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Ledger file '{ledger_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading ledger: {e}")
        sys.exit(1)

    ledger_id = ledger_data.get("ledger_id")
    records = ledger_data.get("records", [])
    pub_key_hex = ledger_data.get("public_key_hex")

    print(f"📄 Ledger ID: {ledger_id}")
    print(f"📊 Total Entries: {len(records)}")
    print("-" * 68)

    try:
        pub_key_bytes = bytes.fromhex(pub_key_hex)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
        print("🔑 Verification Key (Ed25519): LOADED & VALID")
    except Exception as e:
        print(f"❌ Failed to parse public key: {e}")
        sys.exit(1)

    chain_valid = True
    signatures_valid = True
    approved_count = 0

    for i, entry in enumerate(records):
        req_id = entry.get("request_id")
        decision = entry.get("decision")
        curr_hash = entry.get("current_hash")
        prev_hash = entry.get("previous_hash")
        sig_hex = entry.get("signature_hex")

        # 1. Verify Hash Continuity
        hash_link_ok = True
        if i == 0:
            if prev_hash != "0" * 64:
                hash_link_ok = False
        else:
            if prev_hash != records[i - 1]["current_hash"]:
                hash_link_ok = False

        # 2. Recompute Canonical SHA-256 Hash
        check_entry = {k: v for k, v in entry.items() if k not in ["current_hash", "signature_hex"]}
        recomputed_hash = hashlib.sha256(json.dumps(check_entry, sort_keys=True).encode("utf-8")).hexdigest()
        hash_integrity_ok = (recomputed_hash == curr_hash)

        hash_ok = hash_link_ok and hash_integrity_ok
        if not hash_ok:
            chain_valid = False

        # 3. Verify Ed25519 Digital Signature
        try:
            public_key.verify(bytes.fromhex(sig_hex), curr_hash.encode("utf-8"))
            sig_ok = True
        except Exception:
            sig_ok = False
            signatures_valid = False

        if decision == "APPROVED":
            approved_count += 1

        h_status = "✅ PASS" if hash_ok else "❌ BROKEN"
        s_status = "✅ VALID" if sig_ok else "❌ INVALID"
        d_status = "🟢 APPROVED" if decision == "APPROVED" else ("🔴 FLAGGED" if decision == "FLAGGED" else "🟠 ESCALATED")

        print(f"[{i+1:02d}] Req ID: {req_id} | State: {d_status}")
        print(f"     Hash Chain: {h_status} | Signature: {s_status}")
        print(f"     Rationale: {entry.get('justification')}")

    print("-" * 68)
    print("                     FINAL AUDIT SUMMARY                      ")
    print("-" * 68)
    print(f"1. Hash Chain Integrity Check : {'✅ INTACT & PASS' if chain_valid else '❌ TAMPER DETECTED'}")
    print(f"2. Signature Verification     : {'✅ ALL SIGNATURES VALID' if signatures_valid else '❌ SIGNATURE FAILURE'}")
    print(f"3. Automated Approval Rate    : {(approved_count / len(records) * 100):.1f}% ({approved_count}/{len(records)} approved)")
    print("=" * 68)

if __name__ == "__main__":
    verify_ledger()