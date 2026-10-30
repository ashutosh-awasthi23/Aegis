from contextvars import ContextVar
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Role(str, Enum):
    CUSTOMER = "customer"
    INTERN = "intern"
    OPS_ANALYST = "ops_analyst"
    WEALTH_MANAGER = "wealth_manager"
    COMPLIANCE_OFFICER = "compliance_officer"

class SensitivityTier(str, Enum):
    PUBLIC = "public"                 # Safe for Cloud Frontier LLMs
    INTERNAL = "internal"             # Internal policies, non-PII
    RESTRICTED_PII = "restricted_pii" # Strictly routed to Air-Gapped Local GPUs


class SecurityContext(BaseModel):
    """
    Immutable Zero-Trust Envelope attached to every request.
    Carries ABAC attributes, trace IDs, and idempotency keys across all modules.
    """
    trace_id: UUID = Field(default_factory=uuid4)
    idempotency_key: str = Field(
        default_factory=lambda: f"idem_{uuid4().hex}",
        description="Prevents duplicate execution of financial tool calls"
    )
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # ABAC (Attribute-Based Access Control) Identity Attributes
    user_id: str
    role: Role
    branch_id: str = "HQ-BLR-01"
    is_corporate_network: bool = True
    device_trust_score: float = Field(default=1.0, ge=0.0, le=1.0)
    step_up_mfa_verified: bool = False
    assigned_client_ids: list[str] = Field(default_factory=list)

    model_config = {"frozen": True}  # Immutable: no module can tamper with user permissions mid-flight



# Async-safe thread-local storage for the active request context
_current_context: ContextVar[Optional[SecurityContext]] = ContextVar("security_context", default=None)


def set_security_context(ctx: SecurityContext) -> None:
    _current_context.set(ctx)


def get_security_context() -> SecurityContext:
    ctx = _current_context.get()
    if ctx is None:
        raise RuntimeError("Security Violation: Attempted to execute operation without an active SecurityContext!")
    return ctx