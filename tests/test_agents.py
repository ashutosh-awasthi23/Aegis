from aegis.core.context import SecurityContext, Role, set_security_context
from aegis.core.schemas import AegisRequest, SensitivityTier
from aegis.agents.maker_checker import MakerCheckerEngine

# Setup a secure context for the test
ctx = SecurityContext(user_id="emp_882", role=Role.COMPLIANCE_OFFICER)
set_security_context(ctx)

# Create a mock high-risk request
req = AegisRequest(raw_query="Freeze the suspicious account immediately.", sensitivity_tier=SensitivityTier.RESTRICTED_PII)

print("--- Test 1: Maker forgets to cite the policy ---")
# The Maker drafts an action but forgets the crucial citation
bad_draft_action = "Freeze account TOK_ACC_123"
response_1 = MakerCheckerEngine.execute_maker_checker_workflow(req, bad_draft_action)
print(f"Final Status: {response_1.maker_checker_status}")
print(f"System Answer: {response_1.answer}\n")

print("--- Test 2: Maker provides a compliant, cited draft ---")
# The Maker drafts a compliant action with a citation
good_draft_action = "Freeze account TOK_ACC_123 based on AML_POLICY_CITATION (Section 9.1)"
response_2 = MakerCheckerEngine.execute_maker_checker_workflow(req, good_draft_action)
print(f"Final Status: {response_2.maker_checker_status}")
print(f"System Answer: {response_2.answer}")