from aegis.core.context import SecurityContext, Role, set_security_context, get_security_context

# Simulate an intern logging in from a branch terminal
ctx = SecurityContext(
    user_id="emp_9921",
    role=Role.INTERN,
    branch_id="MUM-04",
    is_corporate_network=True
)
set_security_context(ctx)

active = get_security_context()
print(f"Active Trace: {active.trace_id} | Role: {active.role} | Idempotency: {active.idempotency_key}")

# Try to tamper with the role mid-request (This will raise a ValidationError because frozen=True!)
# active.role = Role.COMPLIANCE_OFFICER