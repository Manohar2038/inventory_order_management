class Node:
    def __init__(self, key: int, value: dict):
        self.key = key          # The product_id
        self.value = value      # The product details (e.g., name, price, aisle)
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}  # Hash Map: key -> Node
        
        # Dummy head and tail to avoid edge cases when adding/removing nodes
        self.head = Node(0, {})
        self.tail = Node(0, {})
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node):
        """Always add the new node right after the dummy head (Most Recently Used)."""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node):
        """Move a node to the front to mark it as recently used."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """Pop the current tail (Least Recently Used) to free up capacity."""
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    def get(self, product_id: int):
        """
        Retrieve product details. 
        Time Complexity: $O(1)$
        """
        node = self.cache.get(product_id)
        if not node:
            return None # Cache miss: The system will need to fetch from MySQL
            
        # Cache hit: Move it to the head since it was just used
        self._move_to_head(node)
        return node.value

    def put(self, product_id: int, product_data: dict):
        """
        Add or update a product in the cache. 
        Time Complexity: $O(1)$
        """
        node = self.cache.get(product_id)
        
        if node:
            # Update the value and mark as recently used
            node.value = product_data
            self._move_to_head(node)
        else:
            # Create a new node
            new_node = Node(product_id, product_data)
            self.cache[product_id] = new_node
            self._add_node(new_node)
            
            # Check if we exceeded capacity
            if len(self.cache) > self.capacity:
                # Evict the LRU item from the linked list and the hash map
                lru = self._pop_tail()
                del self.cache[lru.key]

# Quick test block to verify logic
if __name__ == "__main__":
    # Initialize a tiny cache with capacity 3 for testing
    cache = LRUCache(capacity=3)
    
    print("Loading 3 items into the cache...")
    cache.put(1, {"name": "TechPro Keyboard"})
    cache.put(2, {"name": "Nexus Chair"})
    cache.put(3, {"name": "Nova Mouse"})
    
    print(f"Fetch item 1: {cache.get(1)}") # Item 1 is now the most recently used
    
    print("\nAdding item 4. Cache is full, so the least recently used item (Item 2) will be evicted.")
    cache.put(4, {"name": "Giga Monitor"})
    
    print(f"Fetch item 2: {cache.get(2)}") # Should print None (evicted)
    print(f"Fetch item 4: {cache.get(4)}") # Should print data