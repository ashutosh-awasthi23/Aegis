from typing import Dict, Optional
from aegis.core.schemas import AegisRequest, AegisResponse, SensitivityTier
from aegis.core.context import get_security_context


class MakerCheckerEngine:
    """
    Module 5: The Maker-Checker Dual-Control Engine.
    Simulates a multi-agent workflow where an Execution Agent (Maker) drafts 
    an action, and an adversarial Compliance Critic (Checker) reviews it.
    """

    @classmethod
    def execute_maker_checker_workflow(cls, request: AegisRequest, proposed_action: str) -> AegisResponse:
        """
        Runs the dual-control workflow for high-risk actions.
        """
        ctx = get_security_context()
        trace_id = str(ctx.trace_id)

        print(f"--- [MAKER AGENT] Drafting Action: {proposed_action} ---")
        # In production, this would call the LLM to draft the action plan
        maker_draft = f"PROPOSAL: Execute {proposed_action} for trace {trace_id}"

        print(f"--- [CHECKER AGENT] Auditing Maker Draft... ---")
        # The Checker Agent independently evaluates the Maker's draft
        checker_decision = cls._critic_evaluate(maker_draft, request)

        if checker_decision["status"] == "REJECTED":
            return AegisResponse(
                trace_id=trace_id,
                answer=f"Action Blocked by Compliance Critic: {checker_decision['reason']}",
                routed_model="checker-agent-v1",
                sensitivity_tier=request.sensitivity_tier,
                maker_checker_status="REJECTED_BY_CHECKER"
            )

        # If Checker approves, it escalates to a Human Approver
        return AegisResponse(
            trace_id=trace_id,
            answer=f"Draft approved by AI Critic. Escalate to Human Approver for final sign-off.",
            routed_model="maker-checker-pipeline",
            sensitivity_tier=request.sensitivity_tier,
            maker_checker_status="PENDING_HUMAN_SIGNOFF"
        )

    @staticmethod
    def _critic_evaluate(maker_draft: str, request: AegisRequest) -> Dict[str, str]:
        """
        Simulated Checker Agent Logic.
        Rejects actions if they lack citations or violate context rules.
        """
        # Rule 1: A Maker cannot freeze an account without citing a specific AML policy
        if "freeze account" in maker_draft.lower() and "AML_POLICY_CITATION" not in maker_draft:
            return {
                "status": "REJECTED",
                "reason": "Maker attempted to freeze an account without citing an active AML policy constraint."
            }
        
        return {"status": "APPROVED", "reason": "Draft complies with internal regulations."}