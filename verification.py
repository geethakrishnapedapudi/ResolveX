import sqlite3


def verify_refund(action_result):

    if not action_result or not action_result.get("success"):

        return {
            "verified": False,
            "message": "Refund action was not successful."
        }

    connection = sqlite3.connect("resolvex.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, amount
        FROM resolutions
        WHERE action = 'refund'
        ORDER BY id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result and result[0] == "completed":

        return {
            "verified": True,
            "message":
                "Refund successfully verified in the database.",
            "amount": result[1]
        }

    return {
        "verified": False,
        "message":
            "Refund could not be verified in the database."
    }


def verify_replacement(action_result):

    if not action_result or not action_result.get("success"):

        return {
            "verified": False,
            "message":
                "Replacement action was not successful."
        }

    connection = sqlite3.connect("resolvex.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM resolutions
        WHERE action = 'replacement'
        ORDER BY id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result and result[0] == "completed":

        return {
            "verified": True,
            "message":
                "Replacement successfully verified in the database."
        }

    return {
        "verified": False,
        "message":
            "Replacement could not be verified in the database."
    }