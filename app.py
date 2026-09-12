from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
from pathlib import Path

from database import setup_database
from agent import AgentState


class ResolveXServer(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            file_path = Path("templates/index.html")

            html = file_path.read_text(
                encoding="utf-8"
            )

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.end_headers()

            self.wfile.write(
                html.encode("utf-8")
            )

        else:

            self.send_response(404)

            self.end_headers()


    def do_POST(self):

        if self.path == "/resolve":

            length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            data = self.rfile.read(length)

            try:

                request_data = json.loads(
                    data.decode("utf-8")
                )

                customer_request = request_data.get(
                    "request",
                    ""
                ).strip()


                if not customer_request:

                    raise ValueError(
                        "Customer request cannot be empty."
                    )


                order_match = re.search(
                    r"\bORD\d+\b",
                    customer_request.upper()
                )


                if not order_match:

                    response = {

                        "message":
                            "Order information is required.",

                        "order_id":
                            None,

                        "decision":
                            "escalate",

                        "action": {
                            "success": False,
                            "reason":
                                "No order ID was provided."
                        },

                        "verification": {
                            "verified": False,
                            "message":
                                "Task stopped safely because the order could not be identified."
                        },

                        "history": [

                            {
                                "step":
                                    "request_received",

                                "result":
                                    "Customer request received"
                            },

                            {
                                "step":
                                    "understanding_request",

                                "result":
                                    "Analyzing customer intent"
                            },

                            {
                                "step":
                                    "order_identification_failed",

                                "result":
                                    "No valid order ID was found in the request"
                            },

                            {
                                "step":
                                    "safe_stop",

                                "result":
                                    "Agent refused to guess the order"
                            }

                        ]

                    }


                    self.send_response(200)

                    self.send_header(
                        "Content-Type",
                        "application/json"
                    )

                    self.end_headers()

                    self.wfile.write(
                        json.dumps(
                            response
                        ).encode("utf-8")
                    )

                    return


                order_id = order_match.group()


                agent = AgentState(
                    customer_request
                )


                agent.add_history(
                    "request_received",
                    "Customer request received"
                )


                # Understand customer intent first.

                agent.understand_request()


                agent.add_history(
                    "order_identified",
                    "Order ID identified: " + order_id
                )


                agent.investigate_order(
                    order_id
                )


                # Stop safely if the order cannot be found.

                if not agent.order:

                    agent.make_decision()

                    agent.execute_action()

                    agent.adapt()

                    agent.verify_result()

                    response = {

                        "message":
                            "Request escalated safely.",

                        "order_id":
                            order_id,

                        "intent":
                            agent.intent,

                        "decision":
                            agent.decision,

                        "action":
                            agent.action_result,

                        "verification":
                            agent.verification,

                        "history":
                            agent.history

                    }

                else:

                    agent.investigate_policy()

                    agent.investigate_inventory()

                    agent.make_decision()

                    agent.execute_action()

                    agent.adapt()

                    agent.verify_result()


                    response = {

                        "message":
                            "Resolution completed.",

                        "order_id":
                            order_id,

                        "intent":
                            agent.intent,

                        "decision":
                            agent.decision,

                        "action":
                            agent.action_result,

                        "verification":
                            agent.verification,

                        "history":
                            agent.history

                    }


                self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "application/json"
                )

                self.end_headers()

                self.wfile.write(
                    json.dumps(
                        response
                    ).encode("utf-8")
                )


            except Exception as error:

                self.send_response(400)

                self.send_header(
                    "Content-Type",
                    "application/json"
                )

                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "error": str(error)
                    }).encode("utf-8")
                )

        else:

            self.send_response(404)

            self.end_headers()


setup_database()


server = HTTPServer(
    ("localhost", 8000),
    ResolveXServer
)


print(
    "ResolveX is running at http://localhost:8000"
)


server.serve_forever()