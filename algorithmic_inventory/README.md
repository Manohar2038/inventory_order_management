# 📦 Algorithmic Warehouse Management System

A high-performance command-line inventory management system built with Python and MySQL. Unlike standard CRUD applications, this system heavily leverages advanced **Data Structures and Algorithms (DSA)** in the application layer to minimize database load and achieve blazing-fast $O(1)$ and $O(\log n)$ operations.

## 🚀 Key Features & DSA Implementations

*   **Lightning-Fast Autocomplete:** Implemented a custom **Prefix Tree (Trie)** in memory. Instead of querying MySQL with expensive `LIKE '%term%'` operations on every keystroke, searches are resolved in $O(m)$ time (where $m$ is the prefix length).
*   **High-Traffic Caching:** Built a custom **LRU (Least Recently Used) Cache** using a Doubly Linked List paired with a Hash Map. It serves frequently accessed product details instantly in $O(1)$ time, significantly reducing database disk reads.
*   **Dynamic Stock Alerts:** Maintained a **Min-Heap (Priority Queue)** synchronized with a hash map for $O(1)$ lookup of the lowest-stock items. Re-sorting the heap upon inventory transactions takes only $O(\log n)$ time, avoiding full-table database sorts.
*   **Optimized Warehouse Pathfinding:** Modeled the warehouse layout as an **Adjacency List Graph**. Utilized **Dijkstra's Algorithm** paired with a Nearest Neighbor Heuristic to generate the shortest walking paths for multi-item orders.

## 🛠️ Tech Stack
*   **Language:** Python 3.x
*   **Database:** MySQL
*   **Libraries:** `mysql-connector-python`

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/algorithmic_inventory.git](https://github.com/YOUR_USERNAME/algorithmic_inventory.git)
   cd algorithmic_inventory
