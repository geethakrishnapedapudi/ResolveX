import sqlite3

connection = sqlite3.connect("resolvex.db")

cursor = connection.cursor()

cursor.execute(
    """
    UPDATE inventory
    SET quantity = 1
    WHERE product = ?
    """,
    ("Wireless Headphones",)
)

connection.commit()
connection.close()

print("Demo inventory reset to 1")