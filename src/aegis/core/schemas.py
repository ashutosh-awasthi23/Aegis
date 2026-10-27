from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field
from aegis.core.context import SensitivityTier


class Citation(BaseModel):
    """Point-in-time citation from our Temporal GraphRAG pipeline."""
    source_id: str
    document_title: str
    section_clause: str
    effective_from: datetime
    effective_to: Optional[datetime] = None
    snippet: str


class ToolExecutionRecord(BaseModel):
    """Immutable record of an MCP tool or Sandbox calculation."""
    tool_name: str
    idempotency_key: str
    arguments: dict[str, Any]
    result: Any
    required_step_up_auth: bool = False
    executed_at: datetime


class AegisRequest(BaseModel):
    """The standardized payload moving through the Aegis pipeline."""
    raw_query: str
    sanitized_query: Optional[str] = None  # Populated by Format-Preserving Tokenizer
    token_map_id: Optional[str] = None     # Reference to detokenize on client output
    sensitivity_tier: SensitivityTier = SensitivityTier.PUBLIC
    point_in_time_date: Optional[datetime] = None  # For historical policy disputes (e.g., March 12, 2024)


class AegisResponse(BaseModel):
    """The final audited response returned to the user or human approver."""
    trace_id: str
    answer: str
    routed_model: str
    sensitivity_tier: SensitivityTier
    citations: list[Citation] = Field(default_factory=list)
    tool_executions: list[ToolExecutionRecord] = Field(default_factory=list)
    maker_checker_status: Optional[str] = None  # e.g., "APPROVED", "PENDING_HUMAN_SIGNOFF"
    audit_hash: Optional[str] = None            # Cryptographic hash from WORM ledger