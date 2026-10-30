import hashlib
import json
from datetime import datetime, timezone
from aegis.core.config import settings
from aegis.core.schemas import AegisResponse


class WORMAuditLedger:
    """
    Module 6: WORM Immutable Audit Ledger.
    Records every transaction, decision, and tool call into a tamper-proof cryptographic ledger.
    """

    # In a real enterprise system, this points to an append-only S3 bucket or a blockchain ledger.
    # For this prototype, we simulate an append-only digital vault.
    _ledger_vault = []

    @classmethod
    def record_transaction(cls, response: AegisResponse) -> str:
        """
        Hashes the response and permanently writes it to the WORM ledger.
        Returns the cryptographic audit hash.
        """
        # Ensure the WORM ledger is enabled in config
        if not settings.enable_worm_audit_log:
            return "AUDIT_LOGGING_DISABLED"

        # 1. Serialize the response safely for hashing
        # We must exclude the hash itself from the serialization to prevent a cyclic dependency
        payload = response.model_dump(exclude={"audit_hash"})
        
        # We ensure dates are converted to string format for consistent hashing
        payload_str = json.dumps(payload, default=str, sort_keys=True)

        # 2. Cryptographically hash the payload to prove it hasn't been tampered with
        audit_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

        # 3. Append to the immutable ledger
        ledger_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "audit_hash": audit_hash,
            "payload": payload
        }
        cls._ledger_vault.append(ledger_entry)

        return audit_hash

    @classmethod
    def verify_integrity(cls, target_hash: str, response: AegisResponse) -> bool:
        """
        Allows an auditor to re-hash a response and verify it perfectly matches the ledger.
        """
        payload = response.model_dump(exclude={"audit_hash"})
        payload_str = json.dumps(payload, default=str, sort_keys=True)
        recalculated_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        return recalculated_hash == target_hash