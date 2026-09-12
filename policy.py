def check_policy(issue, order_status):

    if order_status != "Delivered":
        return {
            "allowed": False,
            "reason": "Order has not been delivered."
        }

    if issue.lower() == "damaged":
        return {
            "allowed": True,
            "resolution": "replacement_or_refund",
            "reason": "Damaged delivered products are eligible for resolution."
        }

    return {
        "allowed": False,
        "reason": "This issue is not covered by the current policy."
    }