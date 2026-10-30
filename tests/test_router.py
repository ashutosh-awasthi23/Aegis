from aegis.core.context import SecurityContext, Role, set_security_context
from aegis.core.schemas import AegisRequest, SensitivityTier
from aegis.router.router import DataSovereigntyRouter

# Simulate an internal ops analyst querying public info
ctx_public = SecurityContext(user_id="emp_101", role=Role.OPS_ANALYST, is_corporate_network=True)
set_security_context(ctx_public)

req_public = AegisRequest(raw_query="What are the wire cut-off times?", sensitivity_tier=SensitivityTier.PUBLIC)
print("--- Routing Test 1 (Public FAQ) ---")
print(DataSovereigntyRouter.route_request(req_public))

# Simulate a wealth manager querying restricted client portfolio data
ctx_wealth = SecurityContext(user_id="emp_555", role=Role.WEALTH_MANAGER, is_corporate_network=True)
set_security_context(ctx_wealth)

req_pii = AegisRequest(
    raw_query="Show holdings for TOK_ACC_2C2EF7D0CA", 
    sensitivity_tier=SensitivityTier.RESTRICTED_PII
)
print("\n--- Routing Test 2 (Restricted Portfolio PII) ---")
print(DataSovereigntyRouter.route_request(req_pii))