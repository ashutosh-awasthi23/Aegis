from aegis.core.context import SecurityContext, Role, set_security_context
from aegis.mcp_bridges.tools import BankingTools

print("--- Tool Test 1: Deterministic Sandbox Math ---")
# LLM thinks 5.5% on 200k for 15 years is roughly $1500. Let's get the exact penny.
emi = BankingTools.calculate_emi_sandbox(principal=200000, annual_rate=5.5, years=15)
print(f"Exact EMI calculated: ${emi}")


print("\n--- Tool Test 2: Idempotent Wire Transfer ---")
# Set up a fake employee session
ctx = SecurityContext(user_id="emp_007", role=Role.WEALTH_MANAGER)
set_security_context(ctx)

# First attempt by the agent
record_1 = BankingTools.execute_wire_transfer("TOK_ACC_111", "TOK_ACC_999", 50000)
print("Attempt 1 Result:", record_1.result)

# Second attempt (Simulating a network retry glitch by the agent in the same session)
record_2 = BankingTools.execute_wire_transfer("TOK_ACC_111", "TOK_ACC_999", 50000)
print("Attempt 2 Result:", record_2.result)