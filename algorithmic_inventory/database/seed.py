import random
from datetime import datetime, timedelta
from db_connection import DatabaseManager

# Word banks to generate unique product names
ADJECTIVES = ['Wireless', 'Ergonomic', 'Mechanical', 'Smart', 'Portable', 'Bluetooth', 'Heavy Duty', 'Compact', 'RGB', 'Minimalist']
NOUNS = ['Keyboard', 'Mouse', 'Monitor', 'Headset', 'Webcam', 'Microphone', 'Desk', 'Chair', 'Cable', 'Router']
BRANDS = ['TechPro', 'Electro', 'Giga', 'Omni', 'Nova', 'Nexus', 'Apex', 'Vanguard']

def generate_product_name():
    """Generates a random product name like 'TechPro RGB Keyboard'."""
    brand = random.choice(BRANDS)
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{brand} {adj} {noun}"

def seed_database(num_products=150):
    db = DatabaseManager(password='Tvk@2026')
    conn = db.connect()
    
    if not conn:
        print("Failed to connect to the database. Cannot seed.")
        return

    cursor = conn.cursor()

    print(f"Seeding database with {num_products} products...")

    try:
        # Clear existing data to avoid duplicates if run multiple times
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE transactions;")
        cursor.execute("TRUNCATE TABLE inventory;")
        cursor.execute("TRUNCATE TABLE products;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # Track unique names to avoid database unique constraint errors (if any)
        generated_names = set()

        for _ in range(num_products):
            # 1. Generate Product Data
            name = generate_product_name()
            
            # Ensure unique names
            while name in generated_names:
                name = generate_product_name() + f" v{random.randint(2, 9)}"
            generated_names.add(name)

            price = round(random.uniform(10.0, 500.0), 2)
            aisle = f"{random.choice('ABCDEF')}-{random.randint(1, 20)}"

            # Insert Product
            cursor.execute(
                "INSERT INTO products (name, price, aisle_location) VALUES (%s, %s, %s)",
                (name, price, aisle)
            )
            product_id = cursor.lastrowid

            # 2. Generate Inventory Data
            quantity = random.randint(0, 200)
            
            # 30% chance the item has an expiry date (e.g., batteries, perishables)
            if random.random() < 0.3:
                days_to_expire = random.randint(-10, 180) # Some already expired
                expiry_date = (datetime.now() + timedelta(days=days_to_expire)).strftime('%Y-%m-%d')
            else:
                expiry_date = None

            # Insert Inventory
            cursor.execute(
                "INSERT INTO inventory (product_id, quantity, expiry_date) VALUES (%s, %s, %s)",
                (product_id, quantity, expiry_date)
            )

            # 3. Generate a baseline transaction (STOCK_IN) for items with stock
            if quantity > 0:
                cursor.execute(
                    "INSERT INTO transactions (product_id, action, quantity_changed) VALUES (%s, %s, %s)",
                    (product_id, 'STOCK_IN', quantity)
                )

        conn.commit()
        print("Database successfully seeded!")

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    
    finally:
        cursor.close()
        db.close_connection()

if __name__ == "__main__":
    seed_database(200)