import sqlite3

get_inventory_declaration = {
    "name": "get_inventory",
    "description": "Retrieves the inventory list"
}

def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    sql = '''CREATE TABLE IF NOT EXISTS inventory (
       part_id INTEGER PRIMARY KEY,
       part_name TEXT NOT NULL,
       quantity INTEGER NOT NULL,
       price INTEGER NOT NULL
    )'''

    cursor.execute(sql)
    print("Table created successfully")

    conn.close()


def insert_sample_data():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Sample data
    parts = [
        (1, 'Tesla Windshield', 10, 1500),
        (2, 'Porsche Tire', 50, 750),
        (3, 'Porsche Brake Pad', 100, 300),
        (4, 'Tesla Display', 5, 2000),
        (5, 'Tesla Bumper', 5, 2000)
    ]

    cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?)', parts)

    conn.commit()
    conn.close()

def get_inventory():
  
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    query = "SELECT * FROM inventory;"
    cursor.execute(query)

    rows = cursor.fetchall()

    inventory_list = [{"part_id": row[0], "part_name": row[1],
                       "quantity": row[2], "price": row[3]} for row in rows]

    conn.close()

    return inventory_list

# setup_database()
# insert_sample_data()
print(get_inventory())