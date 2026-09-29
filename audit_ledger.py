import hashlib
import json
import time
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class CryptographicAuditLedger:
    def __init__(self):
        self.chain = []
        self.seen_request_ids = set()
        
        # Load or generate Ed25519 keypair locally
        key_env = os.environ.get("AUDIT_PRIVATE_KEY_HEX")
        if key_env:
            self._private_key = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(key_env))
        else:
            self._private_key = ed25519.Ed25519PrivateKey.generate()
            
        self.public_key = self._private_key.public_key()

    def get_public_key_hex(self) -> str:
        raw_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return raw_bytes.hex()

    def record_entry(self, request_id: str, action: str, decision: str, justification: str, memory_id: str, policy_version: str) -> dict:
        # Replay Attack Check
        if request_id in self.seen_request_ids:
            return self.record_entry(
                request_id=f"{request_id}_REPLAY_BLOCKED",
                action=action,
                decision="FLAGGED",
                justification=f"SECURITY_ALERT: Replay attack detected for request_id: {request_id}",
                memory_id=memory_id,
                policy_version=policy_version
            )
            
        self.seen_request_ids.add(request_id)
        prev_hash = self.chain[-1]["current_hash"] if self.chain else "0" * 64
        
        entry = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "request_id": request_id,
            "action": action,
            "decision": decision,
            "justification": justification,
            "hindsight_memory_id": memory_id,
            "policy_version": policy_version,
            "previous_hash": prev_hash
        }
        
        canonical_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        entry["current_hash"] = hashlib.sha256(canonical_bytes).hexdigest()
        
        # Ed25519 Signature over the SHA-256 hash
        sig_bytes = self._private_key.sign(entry["current_hash"].encode("utf-8"))
        entry["signature_hex"] = sig_bytes.hex()
        
        self.chain.append(entry)
        return entry

    def verify_integrity(self) -> tuple[bool, str]:
        """Re-computes every hash and verifies signatures from Genesis block."""
        pubkey = self.public_key
        for i, entry in enumerate(self.chain):
            # Check Hash Link
            if i > 0 and entry["previous_hash"] != self.chain[i-1]["current_hash"]:
                return False, f"Hash link broken at Block #{entry['index']}"
                
            # Recompute Canonical Hash
            check_entry = {k: v for k, v in entry.items() if k not in ["current_hash", "signature_hex"]}
            recomputed_hash = hashlib.sha256(json.dumps(check_entry, sort_keys=True).encode("utf-8")).hexdigest()
            if recomputed_hash != entry["current_hash"]:
                return False, f"Data tampering detected at Block #{entry['index']}: Hash mismatch"
                
            # Verify Signature
            try:
                pubkey.verify(bytes.fromhex(entry["signature_hex"]), entry["current_hash"].encode("utf-8"))
            except Exception:
                return False, f"Invalid signature at Block #{entry['index']}"
                
        return True, "Ledger cryptographically verified."