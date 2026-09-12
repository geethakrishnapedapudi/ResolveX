import sqlite3


def replace_product(product):

    print("\nAttempting replacement...")

    connection = sqlite3.connect("resolvex.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resolutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            action TEXT,
            status TEXT,
            amount REAL
        )
    """)

    # Simulate an unexpected environment change.
    # Inventory was available during investigation,
    # but becomes unavailable before the action executes.

    cursor.execute("""
        UPDATE inventory
        SET quantity = 0
        WHERE product = ?
    """, (product,))

    connection.commit()

    cursor.execute("""
        SELECT quantity
        FROM inventory
        WHERE product = ?
    """, (product,))

    result = cursor.fetchone()

    quantity = result[0] if result else 0

    if quantity <= 0:

        cursor.execute("""
            INSERT INTO resolutions
            (product, action, status, amount)
            VALUES (?, ?, ?, ?)
        """, (
            product,
            "replacement",
            "failed",
            0
        ))

        connection.commit()
        connection.close()

        return {
            "success": False,
            "reason": "Replacement became unavailable.",
            "environment_change":
                "Inventory changed from available to unavailable before execution."
        }


    cursor.execute("""
        UPDATE inventory
        SET quantity = quantity - 1
        WHERE product = ?
    """, (product,))

    cursor.execute("""
        INSERT INTO resolutions
        (product, action, status, amount)
        VALUES (?, ?, ?, ?)
    """, (
        product,
        "replacement",
        "completed",
        0
    ))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Replacement processed successfully."
    }


def issue_refund(amount):

    print("\nIssuing refund...")

    connection = sqlite3.connect("resolvex.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resolutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            action TEXT,
            status TEXT,
            amount REAL
        )
    """)

    cursor.execute("""
        INSERT INTO resolutions
        (product, action, status, amount)
        VALUES (?, ?, ?, ?)
    """, (
        "Wireless Headphones",
        "refund",
        "completed",
        amount
    ))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "amount": amount,
        "message": "Refund processed successfully.",
        "environment_change":
            "Refund transaction recorded."
    }