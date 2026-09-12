from database import get_order
from policy import check_policy
from inventory import check_inventory
from actions import replace_product, issue_refund
from verification import verify_refund, verify_replacement


def get_customer_order(order_id):

    result = get_order(order_id)

    if result:
        return {
            "success": True,
            "order_id": result[0],
            "customer": result[1],
            "product": result[2],
            "status": result[3],
            "issue": result[4],
            "price": result[5]
        }

    return {
        "success": False,
        "reason": "Order could not be found."
    }


def check_resolution_policy(issue, order_status):

    result = check_policy(
        issue,
        order_status
    )

    return result


def check_replacement_inventory(product):

    result = check_inventory(product)

    return result


def execute_replacement(product):

    result = replace_product(product)

    return result


def execute_refund(amount):

    result = issue_refund(amount)

    return result


def verify_final_refund(action_result):

    result = verify_refund(
        action_result
    )

    return result


def verify_final_replacement(action_result):

    result = verify_replacement(
        action_result
    )

    return result