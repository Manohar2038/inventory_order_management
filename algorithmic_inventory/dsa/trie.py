class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        # We store the original casing and DB ID at the leaf node 
        # so we can return useful data to the UI, not just lowercase text.
        self.product_data = [] 

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, product_id: int):
        """
        Inserts a product name into the Trie. 
        Time Complexity: $O(L)$ where L is the length of the word.
        """
        node = self.root
        word_lower = word.lower()  # Normalize for case-insensitive search
        
        for char in word_lower:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
        node.is_end_of_word = True
        node.product_data.append({"id": product_id, "name": word})

    def _dfs(self, node: TrieNode, results: list, limit: int):
        """
        Helper method to perform Depth-First Search to collect words.
        """
        if len(results) >= limit:
            return
            
        if node.is_end_of_word:
            for data in node.product_data:
                results.append(data)
                if len(results) >= limit:
                    return
                    
        for char, child_node in node.children.items():
            self._dfs(child_node, results, limit)

    def get_suggestions(self, prefix: str, limit: int = 10) -> list:
        """
        Returns a list of product dictionaries that start with the prefix.
        Time Complexity: $O(m + K)$ where m is prefix length and K is the number of results.
        """
        node = self.root
        prefix_lower = prefix.lower()
        
        # 1. Traverse down to the end of the prefix
        for char in prefix_lower:
            if char not in node.children:
                return []  # Prefix doesn't exist in the Trie
            node = node.children[char]
            
        # 2. Collect all descendant words from this point using DFS
        results = []
        self._dfs(node, results, limit)
        return results

# Quick test block to verify it works locally
if __name__ == "__main__":
    trie = AutocompleteTrie()
    
    # Simulating data loaded from your MySQL database
    dummy_data = [
        (1, "TechPro RGB Keyboard"),
        (2, "TechPro Wireless Mouse"),
        (3, "Nexus Ergonomic Chair"),
        (4, "TechPro Minimalist Desk"),
        (5, "Nova Mechanical Keyboard")
    ]
    
    for product_id, name in dummy_data:
        trie.insert(name, product_id)
        
    print("Typing 'Tech'...")
    suggestions = trie.get_suggestions("Tech")
    for s in suggestions:
        print(f" - [{s['id']}] {s['name']}")
        
    print("\nTyping 'Nova'...")
    print(trie.get_suggestions("Nova"))