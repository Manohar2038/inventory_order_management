import sys
from core.inventory import InventoryManager

def display_menu():
    print("\n" + "="*45)
    print(" 📦 ALGORITHMIC WAREHOUSE MANAGEMENT SYSTEM ")
    print("="*45)
    print("1. 🔍 Search Product (Trie Autocomplete O(m))")
    print("2. 📋 Get Product Details (LRU Cache O(1))")
    print("3. 📦 Process Stock Transaction (Min-Heap Sync)")
    print("4. 🚨 View Critical Stock Alert (Min-Heap O(1))")
    print("5. 🚪 Exit")
    print("="*45)

def main():
    try:
        # Initialize the system (This triggers the Cold Start warmup)
        manager = InventoryManager()
    except Exception as e:
        print(f"Failed to start system. Did you update your MySQL password? Error: {e}")
        sys.exit(1)

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            prefix = input("Enter product name prefix (e.g., 'Tech'): ").strip()
            print(f"\n--- Autocomplete Results for '{prefix}' ---")
            results = manager.search_products(prefix, limit=10)
            if results:
                for r in results:
                    print(f"ID: {r['id']:<4} | Name: {r['name']}")
            else:
                print("No products found.")

        elif choice == '2':
            try:
                prod_id = int(input("Enter Product ID to fetch: "))
                print("\n--- Product Details ---")
                details = manager.get_product_details(prod_id)
                if details:
                    print(f"Name:     {details['name']}")
                    print(f"Price:    ${details['price']}")
                    print(f"Aisle:    {details['aisle_location']}")
                    print(f"Stock:    {details['quantity']}")
                    if details.get('expiry_date'):
                        print(f"Expires:  {details['expiry_date']}")
                else:
                    print("Product not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == '3':
            try:
                prod_id = int(input("Enter Product ID: "))
                qty_change = int(input("Enter Quantity Change (e.g., 50 for restock, -10 for sale): "))
                action = 'STOCK_IN' if qty_change > 0 else 'STOCK_OUT'
                
                print(f"\nProcessing {action}...")
                success = manager.process_transaction(prod_id, qty_change, action)
                if success:
                    print("Transaction successful! Database, Heap, and Cache updated.")
                else:
                    print("Transaction failed.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")

        elif choice == '4':
            print("\n--- Critical Stock Alert ---")
            critical_item = manager.get_most_critical_stock()
            if critical_item:
                print(f"⚠️ LOWEST STOCK: [{critical_item['id']}] {critical_item['name']} - Only {critical_item['stock']} left!")
            else:
                print("Heap is empty or no stock data available.")

        elif choice == '5':
            print("\nShutting down system. Closing database connection...")
            manager.close()
            print("Goodbye!")
            break
        # ... [Keep existing choices 1 through 4] ...

        elif choice == '5':
            print("\n--- Generate Optimized Pick Route ---")
            raw_ids = input("Enter Product IDs for the order (comma separated, e.g., 5, 12, 45): ")
            try:
                # Convert input string "1, 2, 3" into a list of integers [1, 2, 3]
                product_ids = [int(pid.strip()) for pid in raw_ids.split(",") if pid.strip()]
                
                route, distance, not_found = manager.generate_order_route(product_ids)
                
                if not_found:
                    print(f"⚠️ Warning: Could not find Product IDs: {not_found}")
                    
                if route:
                    print(f"\n✅ Route Generated Successfully!")
                    print(f"🚶 Best Walking Path: {' -> '.join(route)}")
                    print(f"📏 Total Walking Distance: {distance} meters")
                else:
                    print("No valid aisles to visit.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")

        elif choice == '6':
            print("\nShutting down system. Closing database connection...")
            manager.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
        

if __name__ == "__main__":
    main()