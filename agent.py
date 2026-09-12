from database import get_order
from policy import check_policy
from inventory import check_inventory
from actions import replace_product, issue_refund
from verification import verify_refund, verify_replacement
from intent import analyze_request


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


    def add_history(self, step, result):

        self.history.append({
            "step": step,
            "result": result
        })


    def understand_request(self):

        self.add_history(
            "understanding_request",
            "Analyzing what resolution the customer requested"
        )

        self.intent = analyze_request(
            self.customer_request
        )

        self.add_history(
            "request_intent",
            self.intent
        )

        return self.intent


    def investigate_order(self, order_id):

        self.add_history(
            "investigating_order",
            "Looking up order information"
        )

        self.order = get_order(order_id)

        if self.order:

            self.add_history(
                "order_found",
                "Order information retrieved successfully"
            )

        else:

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
            "Checking resolution policy"
        )

        self.policy = check_policy(
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
            "Checking replacement availability"
        )

        self.inventory = check_inventory(product)

        self.add_history(
            "inventory_checked",
            self.inventory
        )

        return self.inventory


    def make_decision(self):

        self.add_history(
            "making_decision",
            "Agent is deciding the best resolution"
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
            "Agent is executing the selected resolution"
        )

        if self.decision == "replacement":

            self.action_result = replace_product(
                self.order[2]
            )

        elif self.decision == "refund":

            self.action_result = issue_refund(
                self.order[5]
            )

        elif self.decision == "escalate":

            self.action_result = {
                "success": False,
                "reason": "Order could not be safely resolved.",
                "escalated": True
            }

        else:

            self.action_result = {
                "success": False,
                "reason": "No valid resolution available."
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

            return

        if self.decision == "escalate":

            self.add_history(
                "adaptation",
                "Agent safely stopped instead of taking an unverified action."
            )

            return

        self.add_history(
            "adaptation",
            "Original action failed. Agent is replanning."
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
            "Verifying the final resolution"
        )

        if self.decision == "refund":

            self.verification = verify_refund(
                self.action_result
            )

        elif self.decision == "replacement":

            self.verification = verify_replacement(
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
                "message": "No resolution to verify."
            }

        self.add_history(
            "verification_result",
            self.verification
        )

        return self.verification


    def show_state(self):

        print("\n--- AGENT STATE ---")

        print("Goal:", self.customer_request)

        print("Intent:", self.intent)

        print("Order:", self.order)

        print("Policy:", self.policy)

        print("Inventory:", self.inventory)

        print("Decision:", self.decision)

        print("Action result:", self.action_result)

        print("Verification:", self.verification)

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