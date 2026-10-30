from datetime import datetime, timezone
from typing import Any
from aegis.core.context import get_security_context
from aegis.core.schemas import ToolExecutionRecord


class BankingTools:
    """
    Module 4: Core Banking MCP (Model Context Protocol) Bridges.
    Exposes strict, idempotent tools for the AI Agent to execute actions safely.
    """

    _executed_transactions : set[str] = set()
    @classmethod
    def execute_wire_transfer(cls, source_account: str, destination_account: str, amount: float) -> ToolExecutionRecord:
        """
        Executes a wire transfer with strict Idempotency checks to prevent double-spending.
        """
        # 1. Grab the active security context for this specific request
        ctx = get_security_context()
        idem_key = ctx.idempotency_key

        # 2. Check for duplicate execution (The FDE Idempotency Shield)
        if idem_key in cls._executed_transactions:
            result_msg = f"SKIPPED: Transaction {idem_key} was already executed."
        else:
            # 3. Simulate calling the real Core Banking API (e.g., Finacle/SWIFT)
            cls._executed_transactions.add(idem_key)
            result_msg = f"SUCCESS: Transferred ${amount:.2f} from {source_account} to {destination_account}."

        # 4. Return the immutable ToolExecutionRecord for the WORM Audit Ledger
        return ToolExecutionRecord(
            tool_name="execute_wire_transfer",
            idempotency_key=idem_key,
            arguments={
                "source": source_account,
                "destination": destination_account,
                "amount": amount
            },
            result=result_msg,
            executed_at=datetime.now(timezone.utc)
        )


    @classmethod
    def calculate_emi_sandbox(cls, principal: float, annual_rate: float, years: int) -> float:
        """
        A Deterministic Calculation Sandbox.
        LLMs are terrible at math. The LLM extracts the variables, but this 
        locked-down Python function calculates the exact penny value.
        """
        if annual_rate == 0:
            return principal / (years * 12)
        
        monthly_rate = (annual_rate / 100) / 12
        months = years * 12
        
        # Standard EMI Formula: P x R x (1+R)^N / [(1+R)^N-1]
        emi = (principal * monthly_rate * ((1 + monthly_rate) ** months)) / (((1 + monthly_rate) ** months) - 1)
        return round(emi, 2)