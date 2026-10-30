from aegis.core.config import settings
from aegis.core.context import SensitivityTier, get_security_context
from aegis.core.schemas import AegisRequest


class DataSovereigntyRouter:
    """
    Module 2: Data-Sovereignty & Cost Router.
    Inspects request sensitivity and content to decide whether to dispatch
    to a low-cost cloud frontier model or an air-gapped local GPU cluster.
    """

    @staticmethod
    def route_request(request: AegisRequest) -> dict[str, str]:
        """
        Determines the appropriate target LLM model and endpoint based on 
        data sensitivity and security context.
        """
        # Pull current zero-trust context (ABAC attributes)
        ctx = get_security_context()

        # Rule 1: If query contains Restricted PII or internal sensitive markers, 
        # it MUST go to our air-gapped local model (Zero external data leakage)
        if request.sensitivity_tier == SensitivityTier.RESTRICTED_PII or not ctx.is_corporate_network:
            return {
                "destination": "AIRGAPPED_LOCAL_CLUSTER",
                "endpoint": settings.airgapped_local_model_url,
                "model_name": "llama3:8b-instruct-fp16", # Local enterprise weights
                "reason": "Restricted PII or external network detected. Locked to on-premise GPUs."
            }

        # Rule 2: For general internal policies or public FAQs, optimize cost 
        # by routing to a fast, inexpensive frontier cloud model
        return {
            "destination": "CLOUD_FRONTIER_API",
            "endpoint": "https://api.openai.com/v1", # or Azure OpenAI endpoint
            "model_name": settings.frontier_cloud_model,
            "reason": "Public/Internal query. Routed to cost-optimized frontier model."
        }