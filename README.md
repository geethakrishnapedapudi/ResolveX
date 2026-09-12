# ResolveX — Autonomous Customer Resolution Agent

## Tech Zephyr 4.0 | Agentic AI Hackathon | IIT Bhubaneswar

ResolveX is an autonomous customer-resolution agent designed to resolve customer issues across simulated enterprise systems.

Instead of only classifying a complaint or generating a response, ResolveX observes the current case state, investigates available information, selects an action, executes the action, observes the result, adapts when conditions change, and verifies the final outcome.

## Problem

Customer-support systems often stop at ticket classification or response generation. Real resolution may require checking multiple systems, making decisions under constraints, executing actions, handling failures, and confirming that the requested outcome actually happened.

ResolveX addresses this workflow using an agentic observe-decide-act-adapt-verify loop.

## Target Use Case

The current prototype focuses on a damaged product replacement/refund scenario.

Example:

"My headphones arrived damaged. Please replace them. Order ORD1001"

The agent investigates the order, policy, and inventory before deciding what action to take.

## Agentic Workflow

```text
Customer Goal
     |
     v
Understand Request
     |
     v
Retrieve Order Information
     |
     v
Check Resolution Policy
     |
     v
Check Inventory
     |
     v
Make Decision
     |
     v
Execute Action
     |
     v
Observe Result
     |
     +---- Action succeeds ----> Verify ----> Final Outcome
     |
     +---- Action fails -------> Replan
                                      |
                                      v
                                  Alternative Action
                                      |
                                      v
                                   Verify
```

## Demonstrated Adaptation

ResolveX intentionally demonstrates a changing environment.

For a damaged product requesting replacement:

1. The agent observes that replacement inventory is available.
2. It selects replacement as the initial resolution.
3. During execution, the simulated inventory changes and replacement becomes unavailable.
4. The agent observes the failed action.
5. It replans from replacement to refund.
6. It executes the refund.
7. It verifies the refund in the resolution database.

This demonstrates goal-driven execution, tool interaction, action-result observation, adaptation, and verification.

## Safe Failure Handling

If the customer request does not contain an order ID, ResolveX does not guess an order.

It safely stops and escalates the case because the order cannot be verified.

## Main Components

* `app.py` — HTTP server and API endpoint
* `agent.py` — agent state, decision process, adaptation and workflow
* `database.py` — customer, order, inventory and resolution data
* `intent.py` — customer-request intent analysis
* `policy.py` — policy eligibility checks
* `inventory.py` — replacement availability tool
* `actions.py` — simulated replacement and refund actions
* `verification.py` — verifies completed actions
* `templates/index.html` — web interface
* `resolvex.db` — local SQLite database created at runtime

## Architecture

```text
Browser
   |
   v
app.py
   |
   v
AgentState
   |
   +--> Intent Analyzer
   |
   +--> Customer / Order Database
   |
   +--> Policy Tool
   |
   +--> Inventory Tool
   |
   +--> Replacement / Refund Tools
   |
   +--> Resolution State
   |
   +--> Verification Tool
   |
   v
Agent History
   |
   v
Browser Timeline
```

## Technology Stack

* Python
* SQLite
* HTML
* CSS
* JavaScript
* Python HTTP Server

The prototype intentionally uses a lightweight stack so the complete agent workflow can be reproduced without requiring large frameworks or infrastructure.

## Requirements

* Python 3.x
* A modern web browser
* VS Code or another code editor

No external Python packages are required for the current prototype.

## Running the Project

Clone or download the repository.

Open a terminal in the ResolveX directory.

Run:

```bash
python app.py
```

The application will start at:

```text
http://localhost:8000
```

Open that address in a browser.

If using the project's virtual environment on Windows:

```bash
venv\Scripts\python.exe app.py
```

## Demo Request

Use:

```text
My headphones arrived damaged. Please replace them. Order ORD1001
```

The expected workflow is:

```text
Replacement selected
        ↓
Replacement becomes unavailable
        ↓
Agent observes failure
        ↓
Agent replans
        ↓
Refund executed
        ↓
Refund verified
```

## Safe-Stop Test

Use:

```text
My headphones arrived damaged. Please replace them.
```

Because no order ID is supplied, the agent should not guess the order and should safely escalate.

## Data and Security

The prototype uses synthetic/demo customer and order information.

No production customer data is required.

Do not commit API keys, passwords, tokens, or confidential credentials to the repository.

The local SQLite database is excluded from Git using `.gitignore`.

## Current Scope

ResolveX currently demonstrates:

* Customer-goal understanding
* Order lookup
* Policy validation
* Inventory checking
* Resolution selection
* State-changing simulated actions
* Failure observation
* Dynamic replanning
* Refund fallback
* Database-backed verification
* Safe escalation
* Agent execution history

## Future Extensions

Potential future extensions include:

* LLM-based natural-language intent understanding
* Additional cancellation workflows
* External enterprise APIs
* Policy retrieval
* More customer/order scenarios
* Automated evaluation and metrics
* Role-based human approval for high-risk actions

## Hackathon Alignment

ResolveX is designed around the Agentic AI requirements of Tech Zephyr 4.0:

**Goal → Observe → Decide → Act → Observe Result → Adapt → Verify**

The prototype demonstrates a complete workflow rather than a one-shot generated response.
