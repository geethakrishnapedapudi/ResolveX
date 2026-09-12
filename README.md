# ResolveX
## Autonomous Customer Resolution Agent

> From complaint to verified resolution — autonomously.

ResolveX is an Agentic AI customer-resolution system that understands a
customer request, investigates the order, checks policy and inventory,
selects a resolution, executes it, observes the result, adapts when the
environment changes, and verifies the final outcome.

## Agentic Workflow

Customer Goal
→ Understand
→ Investigate Order
→ Check Policy
→ Check Inventory
→ Decide
→ Act
→ Observe
→ Adapt/Replan
→ Verify
→ Final Resolution

## Example

Customer:
"My headphones arrived damaged. Please replace them. Order ORD1001."

The agent:

1. Uses Gemini to understand the request.
2. Retrieves the customer and order.
3. Checks the resolution policy.
4. Checks replacement inventory.
5. Selects replacement.
6. Attempts the replacement.
7. Detects that inventory became unavailable.
8. Observes the failed action.
9. Autonomously replans to a refund.
10. Executes the refund.
11. Verifies the refund in SQLite.

Result:

Replacement → Failure → Replan → Refund → Verified

## Technology

- Python
- Gemini API
- SQLite
- HTML/CSS/JavaScript
- Google GenAI SDK

## Core Components

- `agent.py` — agent state and orchestration
- `tools.py` — agent tool interface
- `database.py` — persistent application state
- `policy.py` — resolution policy
- `inventory.py` — inventory tool
- `actions.py` — replacement/refund actions
- `verification.py` — final-state verification
- `intent.py` — intent fallback
- `app.py` — web application

## Run

Install dependencies:

```bash
pip install -U google-genai python-dotenv