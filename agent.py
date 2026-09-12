import os
import json

from dotenv import load_dotenv
from google import genai

from tools import (
    get_customer_order,
    check_resolution_policy,
    check_replacement_inventory,
    execute_replacement,
    execute_refund,
    verify_final_refund,
    verify_final_replacement
)

from database import save_agent_event
from intent import analyze_request


load_dotenv()


class AgentState:

    def __init__(self, customer_request):

        self.customer_request = customer_request

        self.intent = None

        self.order = None
        self.policy = None
        self.inventory = None

        self.decision = None
        self.action_result = None
        self.verification = None

        self.history = []

        self.ai_reasoning = None

        self.gemini_available = bool(
            os.getenv("GEMINI_API_KEY")
        )


    def add_history(self, step, result):

        event = {
            "step": step,
            "result": result
        }

        self.history.append(event)

        try:

            save_agent_event(
                step,
                str(result)
            )

        except Exception as error:

            print(
                "Could not save agent event:",
                error
            )


    def understand_request(self):

        self.add_history(
            "understanding_request",
            "Analyzing customer intent"
        )

        # First use the deterministic intent detector.
        self.intent = analyze_request(
            self.customer_request
        )

        # Use Gemini to understand the request and explain
        # the reasoning behind the requested resolution.
        if self.gemini_available:

            try:

                client = genai.Client(
                    api_key=os.getenv("GEMINI_API_KEY")
                )

                prompt = f"""
You are the reasoning layer of ResolveX,
an autonomous customer resolution agent.

Customer request:
{self.customer_request}

Identify:
1. customer intent
2. issue
3. requested resolution
4. concise reasoning

Possible intents:
replacement, refund, cancellation, unknown.

Return ONLY valid JSON in this format:

{{
  "intent": "replacement",
  "issue": "damaged product",
  "requested_resolution": "replacement",
  "reasoning": "Customer explicitly requested a replacement."
}}
"""

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                ai_text = response.text.strip()

                # Remove accidental markdown fences.
                if ai_text.startswith("```"):

                    ai_text = ai_text.replace(
                        "```json",
                        ""
                    ).replace(
                        "```",
                        ""
                    ).strip()

                self.ai_reasoning = json.loads(
                    ai_text
                )

                self.add_history(
                    "gemini_reasoning",
                    self.ai_reasoning
                )

                # Gemini can improve the detected intent,
                # but downstream tools remain authoritative.
                if self.ai_reasoning.get("intent"):

                    self.intent = {
                        "intent":
                            self.ai_reasoning["intent"],

                        "reason":
                            self.ai_reasoning.get(
                                "reasoning",
                                "Gemini analyzed the request."
                            )
                    }

            except Exception as error:

                self.add_history(
                    "gemini_fallback",
                    "Gemini unavailable. Using deterministic intent analysis."
                )

                print(
                    "Gemini error:",
                    error
                )

        else:

            self.add_history(
                "gemini_fallback",
                "Gemini API key unavailable. Using deterministic intent analysis."
            )

        self.add_history(
            "request_intent",
            self.intent
        )

        return self.intent


    def investigate_order(self, order_id):

        self.add_history(
            "investigating_order",
            "Agent is using the customer/order tool"
        )

        order_data = get_customer_order(
            order_id
        )

        if order_data["success"]:

            self.order = (
                order_data["order_id"],
                order_data["customer"],
                order_data["product"],
                order_data["status"],
                order_data["issue"],
                order_data["price"]
            )

            self.add_history(
                "order_found",
                "Customer and order information retrieved successfully"
            )

        else:

            self.order = None

            self.add_history(
                "order_not_found",
                "Order " + order_id + " could not be found"
            )

            self.decision = "escalate"

            self.add_history(
                "safe_stop",
                "Agent stopped because the order could not be verified"
            )

        return self.order


    def investigate_policy(self):

        if not self.order:

            return None

        self.add_history(
            "checking_policy",
            "Agent is using the policy tool"
        )

        self.policy = check_resolution_policy(
            self.order[4],
            self.order[3]
        )

        self.add_history(
            "policy_checked",
            self.policy
        )

        return self.policy


    def investigate_inventory(self):

        if not self.order:

            return None

        product = self.order[2]

        self.add_history(
            "checking_inventory",
            "Agent is using the inventory tool"
        )

        self.inventory = check_replacement_inventory(
            product
        )

        self.add_history(
            "inventory_checked",
            self.inventory
        )

        return self.inventory


    def make_decision(self):

        self.add_history(
            "making_decision",
            "Agent is evaluating intent, policy and available options"
        )

        if self.decision == "escalate":

            self.add_history(
                "decision_made",
                "escalate"
            )

            return self.decision

        if not self.policy or not self.policy["allowed"]:

            self.decision = "reject"

        elif self.intent and self.intent["intent"] == "refund":

            self.decision = "refund"

        elif (
            self.intent
            and self.intent["intent"] == "replacement"
            and self.inventory
            and self.inventory["available"]
        ):

            self.decision = "replacement"

        elif (
            self.intent
            and self.intent["intent"] == "replacement"
        ):

            self.decision = "refund"

            self.add_history(
                "fallback_decision",
                "Replacement unavailable during investigation. Refund selected."
            )

        else:

            self.decision = "escalate"

        self.add_history(
            "decision_made",
            self.decision
        )

        return self.decision


    def execute_action(self):

        self.add_history(
            "executing_action",
            "Agent selected a tool and is executing the resolution"
        )

        if self.decision == "replacement":

            self.action_result = execute_replacement(
                self.order[2]
            )

        elif self.decision == "refund":

            self.action_result = execute_refund(
                self.order[5]
            )

        elif self.decision == "escalate":

            self.action_result = {
                "success": False,
                "reason":
                    "Order could not be safely resolved.",
                "escalated": True
            }

        else:

            self.action_result = {
                "success": False,
                "reason":
                    "No valid resolution available."
            }

        self.add_history(
            "action_result",
            self.action_result
        )

        return self.action_result


    def adapt(self):

        if not self.action_result:

            return

        if self.action_result.get("success"):

            self.add_history(
                "adaptation",
                "Action succeeded. No replanning was required."
            )

            return

        if self.decision == "escalate":

            self.add_history(
                "adaptation",
                "Agent safely stopped instead of taking an unverified action."
            )

            return

        self.add_history(
            "adaptation",
            "Original action failed. Agent observed the failure and is replanning."
        )

        if self.decision == "replacement":

            self.decision = "refund"

            self.add_history(
                "replanned",
                "Agent changed resolution from replacement to refund"
            )

            self.execute_action()


    def verify_result(self):

        self.add_history(
            "verification",
            "Agent is using the verification tool to check the final outcome"
        )

        if self.decision == "refund":

            self.verification = verify_final_refund(
                self.action_result
            )

        elif self.decision == "replacement":

            self.verification = verify_final_replacement(
                self.action_result
            )

        elif self.decision == "escalate":

            self.verification = {
                "verified": False,
                "message":
                    "Task was safely escalated because the request could not be safely resolved."
            }

        else:

            self.verification = {
                "verified": False,
                "message":
                    "No resolution to verify."
            }

        self.add_history(
            "verification_result",
            self.verification
        )

        return self.verification


    def show_state(self):

        print("\n--- AGENT STATE ---")

        print(
            "Goal:",
            self.customer_request
        )

        print(
            "Intent:",
            self.intent
        )

        print(
            "Gemini reasoning:",
            self.ai_reasoning
        )

        print(
            "Order:",
            self.order
        )

        print(
            "Policy:",
            self.policy
        )

        print(
            "Inventory:",
            self.inventory
        )

        print(
            "Decision:",
            self.decision
        )

        print(
            "Action result:",
            self.action_result
        )

        print(
            "Verification:",
            self.verification
        )

        print("\nHistory:")

        for item in self.history:

            print(item)


if __name__ == "__main__":

    agent = AgentState(
        "My headphones arrived damaged. Please replace them. Order ORD1001"
    )

    agent.add_history(
        "request_received",
        "Customer request received"
    )

    agent.understand_request()

    agent.investigate_order(
        "ORD1001"
    )

    agent.investigate_policy()

    agent.investigate_inventory()

    agent.make_decision()

    agent.execute_action()

    agent.adapt()

    agent.verify_result()

    agent.show_state()