# ResolveX

## Autonomous Customer Resolution Agent

**Team:** SPECTRIX
**Hackathon:** Tech Zephyr 4.0 — Agentic AI Hackathon
**Institution:** IIT Bhubaneswar
**Problem Statement:** PS5 — Autonomous Customer Resolution Agent

### 1. Problem Statement

Customer-support systems often stop at ticket classification or generating a response. The real challenge is completing the customer's requested resolution across multiple enterprise systems.

A resolution may depend on order status, customer information, policy rules, inventory availability, and the success of a state-changing action. These conditions can also change while the resolution is being executed.

ResolveX addresses this problem by autonomously pursuing the customer's resolution goal rather than merely recommending what a support executive should do.

### 2. Target Users

* E-commerce customer-support teams
* Customer-service operations
* Support managers
* Businesses handling high-volume order issues

### 3. Why Agentic AI?

This problem requires more than a chatbot or fixed workflow because the correct action cannot always be known in advance.

ResolveX follows a closed-loop agentic process:

**OBSERVE → DECIDE → ACT → OBSERVE → ADAPT → VERIFY**

The agent:

* Understands the customer's goal.
* Retrieves relevant case information.
* Evaluates policy and constraints.
* Selects an appropriate resolution.
* Executes a state-changing action.
* Observes the actual result.
* Replans when conditions change or an action fails.
* Verifies the final state.

This directly demonstrates the required agentic characteristics of goal-driven execution, dynamic action selection, multi-step execution, adaptation, and robustness.

### 4. Proposed Solution

ResolveX is an autonomous customer-resolution agent connected to simulated enterprise tools.

For each customer request, ResolveX:

1. Understands the customer's requested resolution.
2. Identifies and retrieves the relevant order.
3. Checks the applicable resolution policy.
4. Checks replacement inventory.
5. Selects the best available resolution.
6. Executes the selected action.
7. Observes the intermediate result.
8. Detects failures or changed constraints.
9. Replans when necessary.
10. Executes the revised resolution.
11. Verifies the final outcome.

The system uses persistent application state and records agent events throughout the workflow.

### 5. Demonstration Scenario

**Customer request:**

"My headphones arrived damaged. Please replace them. Order ORD1001."

Initially, ResolveX determines that replacement is appropriate and inventory is available.

During execution, the simulated environment changes and the replacement becomes unavailable.

Instead of stopping or returning a generic failure, ResolveX:

**Replacement selected**
↓
**Replacement fails**
↓
**Environment change observed**
↓
**Agent replans**
↓
**Refund selected**
↓
**Refund executed**
↓
**Refund verified**

This demonstrates the required failure/changed-condition behavior specified for PS5.

### 6. Technical Approach

**Reasoning Layer**

* Gemini API
* Request understanding
* Resolution reasoning

**Agent State**

* Customer request
* Order information
* Policy result
* Inventory state
* Decision
* Action result
* Verification result
* Execution history

**Tools**

* Customer/order lookup
* Policy evaluation
* Inventory lookup
* Replacement execution
* Refund execution
* Outcome verification

**Environment**

* SQLite-based simulated enterprise state
* State-changing resolution actions

**Interface**

* Web-based ResolveX application

### 7. Expected Impact

ResolveX aims to reduce the manual effort required for routine customer-resolution workflows by allowing an agent to move from **customer complaint → verified resolution**.

Potential benefits include:

* Faster resolution of routine cases
* Reduced repetitive support workload
* Consistent policy-based decisions
* Automatic recovery from operational failures
* Better visibility through execution history
* Reduced risk of falsely claiming successful resolution through final-state verification

### 8. Key Differentiator

ResolveX does not simply **recommend** a resolution.

It **pursues the resolution, interacts with the environment, reacts to failure, changes its plan, executes the alternative, and verifies the final result.**

**Complaint → Decision → Action → Failure → Adaptation → Verified Resolution**

This closed-loop behavior is the core of ResolveX.
