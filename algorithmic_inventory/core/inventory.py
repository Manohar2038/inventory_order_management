import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import DatabaseManager
from dsa.trie import AutocompleteTrie
from dsa.min_heap import MinHeap
from dsa.lru_cache import LRUCache
from dsa.graph import WarehouseGraph 

class InventoryManager:
    def __init__(self):
        print("Initializing Algorithmic Inventory Manager...")
        self.db_manager = DatabaseManager(password='YOUR_MYSQL_PASSWORD') # Update password
        self.conn = self.db_manager.connect()
        
        # Initialize Data Structures
        self.trie = AutocompleteTrie()
        self.low_stock_heap = MinHeap()
        self.cache = LRUCache(capacity=50) # Cache the 50 most viewed products
        
        # Cold Start: Load DB data into memory
        self._warmup_dsa()

    def _warmup_dsa(self):
        """Fetches initial data from MySQL to populate the Trie and Min-Heap on startup."""
        if not self.conn:
            print("Database connection failed. Cannot warm up data structures.")
            return

        cursor = self.conn.cursor(dictionary=True)
        # Fetch product names for Trie, and stock quantities for Min-Heap
        query = """
            SELECT p.id, p.name, i.quantity 
            FROM products p 
            JOIN inventory i ON p.id = i.product_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            # 1. Populate Trie for autocomplete
            self.trie.insert(row['name'], row['id'])
            
            # 2. Populate Min-Heap for low stock alerts (Priority = quantity)
            self.low_stock_heap.insert(row['id'], row['name'], row['quantity'])
            
        cursor.close()
        print(f"System ready! Loaded {len(rows)} products into memory.")

    def search_products(self, prefix: str, limit: int = 5):
        """Searches via Trie instead of MySQL. Blazing fast O(m)."""
        return self.trie.get_suggestions(prefix, limit)

    def get_product_details(self, product_id: int):
        """Fetches product details. Tries LRU Cache first, falls back to MySQL."""
        # 1. Check Cache (O(1) Memory Lookup)
        cached_data = self.cache.get(product_id)
        if cached_data:
            print("[CACHE HIT] Fetching from Memory")
            return cached_data

        # 2. Cache Miss: Query Database (Slower Disk Lookup)
        print("[CACHE MISS] Fetching from MySQL")
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT p.id, p.name, p.price, p.aisle_location, i.quantity, i.expiry_date 
            FROM products p 
            JOIN inventory i ON p.id = i.product_id 
            WHERE p.id = %s
        """
        cursor.execute(query, (product_id,))
        product_data = cursor.fetchone()
        cursor.close()

        if product_data:
            # 3. Store in Cache for next time
            self.cache.put(product_id, product_data)
            
        return product_data

    def process_transaction(self, product_id: int, quantity_change: int, action: str):
        """Updates stock in MySQL, the Min-Heap, and invalidates the cache."""
        cursor = self.conn.cursor()
        try:
            # 1. Update MySQL Inventory
            cursor.execute(
                "UPDATE inventory SET quantity = quantity + %s WHERE product_id = %s",
                (quantity_change, product_id)
            )
            
            # 2. Log MySQL Transaction
            cursor.execute(
                "INSERT INTO transactions (product_id, action, quantity_changed) VALUES (%s, %s, %s)",
                (product_id, action, quantity_change)
            )
            
            # Fetch the new total quantity to update the heap
            cursor.execute("SELECT quantity, name FROM inventory JOIN products ON id = product_id WHERE product_id = %s", (product_id,))
            new_quantity, name = cursor.fetchone()
            
            self.conn.commit()

            # 3. Update Min-Heap in O(log n) time
            self.low_stock_heap.update_priority(product_id, new_quantity)

            # 4. Update Cache (if this item is currently cached, its stock data is now stale)
            cached_item = self.cache.get(product_id)
            if cached_item:
                cached_item['quantity'] = new_quantity
                self.cache.put(product_id, cached_item)

            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"Transaction failed: {e}")
            return False
        finally:
            cursor.close()

    def get_most_critical_stock(self):
        """Returns the item closest to running out of stock instantly O(1)."""
        critical_node = self.low_stock_heap.peek()
        if critical_node:
            return {"id": critical_node.product_id, "name": critical_node.name, "stock": critical_node.priority_value}
        return None

    def close(self):
        self.db_manager.close_connection()