from aegis.core.schemas import AegisResponse, SensitivityTier
from aegis.governance.worm_ledger import WORMAuditLedger

# Simulate a completed Maker-Checker response
mock_response = AegisResponse(
    trace_id="trace_9999",
    answer="Draft approved by AI Critic. Escalate to Human Approver for final sign-off.",
    routed_model="maker-checker-pipeline",
    sensitivity_tier=SensitivityTier.RESTRICTED_PII,
    maker_checker_status="PENDING_HUMAN_SIGNOFF"
)

print("--- Test 1: Writing to the WORM Ledger ---")
# 1. Record it to the ledger and get the tamper-proof hash
cryptographic_hash = WORMAuditLedger.record_transaction(mock_response)
mock_response.audit_hash = cryptographic_hash

print(f"Transaction recorded successfully.")
print(f"Audit Hash: {cryptographic_hash}")


print("\n--- Test 2: Auditor Integrity Check ---")
# 2. An auditor comes in a year later and checks the integrity of the record
is_valid = WORMAuditLedger.verify_integrity(cryptographic_hash, mock_response)
print(f"Auditor Integrity Check Passed? {is_valid}")