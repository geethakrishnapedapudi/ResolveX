import sqlite3


def setup_database():

    connection = sqlite3.connect("resolvex.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            product TEXT,
            status TEXT,
            issue TEXT,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            product TEXT PRIMARY KEY,
            quantity INTEGER
        )
    """)

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
        CREATE TABLE IF NOT EXISTS agent_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step TEXT,
            result TEXT
        )
    """)


    cursor.execute("""
        INSERT OR IGNORE INTO customers
        VALUES (
            'C001',
            'Rahul',
            'rahul@example.com'
        )
    """)


    cursor.execute("""
        INSERT OR IGNORE INTO orders
        VALUES (
            'ORD1001',
            'C001',
            'Wireless Headphones',
            'Delivered',
            'Damaged',
            2999
        )
    """)


    # Reset demo inventory for every server start.

    cursor.execute("""
        INSERT OR REPLACE INTO inventory
        VALUES (
            'Wireless Headphones',
            1
        )
    """)


    connection.commit()

    connection.close()


def get_order(order_id):

    connection = sqlite3.connect("resolvex.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            orders.order_id,
            customers.name,
            orders.product,
            orders.status,
            orders.issue,
            orders.price
        FROM orders
        JOIN customers
        ON orders.customer_id = customers.customer_id
        WHERE orders.order_id = ?
    """, (order_id,))

    result = cursor.fetchone()

    connection.close()

    return result


def save_agent_event(step, result):

    connection = sqlite3.connect("resolvex.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO agent_events
        (step, result)
        VALUES (?, ?)
    """, (
        step,
        result
    ))

    connection.commit()

    connection.close()


if __name__ == "__main__":

    setup_database()

    order = get_order(
        "ORD1001"
    )

    print("Order information:")
    print(order)

    save_agent_event(
        "test",
        "Agent event storage is working."
    )

    print(
        "Agent event saved successfully."
    )