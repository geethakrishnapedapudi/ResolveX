import sqlite3


def check_inventory(product):

    connection = sqlite3.connect("resolvex.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            product TEXT PRIMARY KEY,
            quantity INTEGER
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO inventory
        VALUES ('Wireless Headphones', 1)
    """)

    connection.commit()

    cursor.execute("""
        SELECT quantity
        FROM inventory
        WHERE product = ?
    """, (product,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return {
            "available": result[0] > 0,
            "quantity": result[0]
        }

    return {
        "available": False,
        "quantity": 0
    }


if __name__ == "__main__":

    result = check_inventory("Wireless Headphones")

    print("Inventory result:")
    print(result)