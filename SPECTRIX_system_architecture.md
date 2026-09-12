# ResolveX — System Architecture & Workflow

## 1. High-Level Architecture

Customer
   ↓
ResolveX Web Interface
   ↓
Agent Orchestrator
   ↓
┌─────────────────────────────────────┐
│        Agent State & Planning       │
│                                     │
│ Goal → Context → Decision → Action  │
│        → Observation → Adaptation   │
│        → Verification               │
└─────────────────────────────────────┘
   ↓
Tool Layer
   ├── Customer / Order Tool
   ├── Policy Tool
   ├── Inventory Tool
   ├── Replacement Tool
   ├── Refund Tool
   └── Verification Tool
   ↓
SQLite Application Environment
   ├── Customers
   ├── Orders
   ├── Inventory
   ├── Resolutions
   └── Agent Events

## 2. Agentic Execution Loop

### Step 1 — Goal Understanding

The agent receives the customer's request and identifies the
requested resolution using Gemini reasoning with deterministic
fallback logic.

### Step 2 — Investigation

The agent retrieves:

- Customer information
- Order information
- Order status
- Reported issue
- Product information
- Product price

### Step 3 — Policy Evaluation

The policy tool determines whether the requested issue is eligible
for resolution and identifies permitted resolution options.

### Step 4 — Environment Inspection

The agent checks current inventory before selecting a replacement.

### Step 5 — Decision

The agent evaluates the current state and selects an action:

- Replacement
- Refund
- Escalation

### Step 6 — Tool Execution

The selected resolution tool performs a state-changing operation
in the simulated enterprise environment.

### Step 7 — Observation

The agent receives the actual result of the action.

The result may differ from the earlier investigation because the
environment can change during execution.

### Step 8 — Adaptation & Replanning

If the selected action fails, the agent does not blindly retry.

It observes the failure, updates its state, and selects an
alternative resolution when it is safe to do so.

### Step 9 — Verification

The verification tool checks the persistent application state
to confirm that the intended resolution was actually completed.

### Step 10 — Final Outcome

The agent returns the verified resolution and execution history
to the user.

## 3. Example Failure-Recovery Workflow

Customer Goal:
"Replace my damaged headphones. Order ORD1001."

        ↓

Understand Request
        ↓

Retrieve Order
        ↓

Check Policy
        ↓

Check Inventory
        ↓

Decision: REPLACEMENT
        ↓
Execute Replacement
        ↓
Inventory Changes Unexpectedly
        ↓
Replacement Fails
        ↓
Observe Failure
        ↓
Replan
        ↓
Decision: REFUND
        ↓
Execute Refund
        ↓
Verify Refund
        ↓
FINAL: VERIFIED REFUND

## 4. State Maintained by the Agent

The agent maintains task state including:

- Customer request
- Intent
- Order information
- Policy result
- Inventory result
- Current decision
- Action result
- Verification result
- Execution history
- Gemini reasoning

This allows the agent to make decisions based on the current
workflow state rather than treating each step as an isolated
LLM response.

## 5. Tool Responsibilities

### Customer / Order Tool
Retrieves and validates customer and order information.

### Policy Tool
Determines whether the reported issue is eligible for resolution.

### Inventory Tool
Checks current replacement availability.

### Replacement Tool
Attempts the replacement and records the resulting state.

### Refund Tool
Executes and records the refund transaction.

### Verification Tool
Checks the persistent state after an action to confirm completion.

## 6. Failure Handling

### Missing Order

Detection:
Order lookup returns no valid order.

Response:
The agent safely stops and escalates rather than guessing.

### Replacement Unavailable

Detection:
Replacement execution reports that inventory became unavailable.

Response:
The agent observes the failure and replans to a refund.

### Gemini Failure

Detection:
Gemini request fails or returns unusable output.

Response:
ResolveX falls back to deterministic intent analysis so the
core workflow can continue.

### Verification Failure

Detection:
The expected completed state cannot be found.

Response:
The resolution is not reported as successfully verified.

## 7. Agentic Principle

ResolveX implements:

**OBSERVE → DECIDE → ACT → OBSERVE → ADAPT → ACT → VERIFY**

The key distinction from a chatbot or fixed workflow is that the
agent can respond to an unexpected intermediate result and change
its plan before producing the final outcome.