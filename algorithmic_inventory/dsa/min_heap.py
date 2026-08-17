class HeapNode:
    def __init__(self, product_id: int, name: str, priority_value: int):
        self.product_id = product_id
        self.name = name
        self.priority_value = priority_value  # Can be quantity, or days until expiry

    def __repr__(self):
        return f"[{self.priority_value}] {self.name} (ID: {self.product_id})"


class MinHeap:
    def __init__(self):
        self.heap = []
        # The secret weapon for interviews: A hash map tracking the exact array 
        # index of every product_id. This makes updates O(log n) instead of O(n).
        self.position_map = {}

    def _swap(self, i: int, j: int):
        """Swaps two nodes and updates their positions in the position_map."""
        # Swap the actual nodes
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
        # Update the hash map with their new indices
        self.position_map[self.heap[i].product_id] = i
        self.position_map[self.heap[j].product_id] = j

    def _heapify_up(self, index: int):
        parent_index = (index - 1) // 2
        if parent_index >= 0 and self.heap[parent_index].priority_value > self.heap[index].priority_value:
            self._swap(index, parent_index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index: int):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        n = len(self.heap)

        if left_child < n and self.heap[left_child].priority_value < self.heap[smallest].priority_value:
            smallest = left_child

        if right_child < n and self.heap[right_child].priority_value < self.heap[smallest].priority_value:
            smallest = right_child

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def insert(self, product_id: int, name: str, priority_value: int):
        """Inserts a new item into the heap in O(log n) time."""
        if product_id in self.position_map:
            # If it already exists, just update its value
            self.update_priority(product_id, priority_value)
            return

        node = HeapNode(product_id, name, priority_value)
        self.heap.append(node)
        index = len(self.heap) - 1
        self.position_map[product_id] = index
        self._heapify_up(index)

    def extract_min(self) -> HeapNode:
        """Removes and returns the item with the lowest priority value in O(log n) time."""
        if not self.heap:
            return None
            
        if len(self.heap) == 1:
            node = self.heap.pop()
            del self.position_map[node.product_id]
            return node

        # Swap root with the last element
        min_node = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.position_map[self.heap[0].product_id] = 0
        del self.position_map[min_node.product_id]
        
        # Restore heap property
        self._heapify_down(0)
        return min_node

    def peek(self) -> HeapNode:
        """Returns the item with the lowest priority value in O(1) time without removing it."""
        return self.heap[0] if self.heap else None

    def update_priority(self, product_id: int, new_priority: int):
        """
        Updates an item's priority and restores the heap. 
        Because of position_map, finding the item is O(1) and moving it is O(log n).
        """
        if product_id not in self.position_map:
            return

        index = self.position_map[product_id]
        old_priority = self.heap[index].priority_value
        self.heap[index].priority_value = new_priority

        if new_priority < old_priority:
            self._heapify_up(index)
        elif new_priority > old_priority:
            self._heapify_down(index)


# Quick test block
if __name__ == "__main__":
    low_stock_heap = MinHeap()
    
    # Simulating stock levels (Priority = Quantity)
    print("Loading stock into the Min-Heap...")
    low_stock_heap.insert(1, "TechPro Keyboard", 45)
    low_stock_heap.insert(2, "Nexus Chair", 5)
    low_stock_heap.insert(3, "Nova Mouse", 12)
    low_stock_heap.insert(4, "Giga Monitor", 2)
    
    print(f"Most critical item to restock: {low_stock_heap.peek()}")
    
    print("\nSimulating a massive restock of Giga Monitors (Quantity 2 -> 50)...")
    low_stock_heap.update_priority(4, 50)
    
    print(f"New most critical item: {low_stock_heap.peek()}")