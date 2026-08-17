import heapq

class WarehouseGraph:
    def __init__(self):
        # Adjacency list representation: {node: {neighbor: weight}}
        self.graph = {}

    def add_location(self, node: str):
        """Registers an aisle or intersection in the warehouse."""
        if node not in self.graph:
            self.graph[node] = {}

    def add_path(self, node1: str, node2: str, distance: int):
        """Adds a bidirectional path (edge) between two warehouse locations."""
        self.add_location(node1)
        self.add_location(node2)
        self.graph[node1][node2] = distance
        self.graph[node2][node1] = distance # Assuming workers can walk both ways

    def dijkstra(self, start_node: str):
        """
        Calculates the shortest paths from the start_node to all other nodes.
        Time Complexity: O(E log V) where E is edges and V is vertices.
        """
        distances = {node: float('infinity') for node in self.graph}
        distances[start_node] = 0
        previous_nodes = {node: None for node in self.graph}
        
        # Priority Queue: (cumulative_distance, node)
        pq = [(0, start_node)]
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # If we process an outdated, longer path in the queue, skip it
            if current_distance > distances[current_node]:
                continue
                
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                
                # Only consider this new path if it's strictly shorter
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
                    
        return distances, previous_nodes

    def get_shortest_path(self, start: str, end: str):
        """Reconstructs the precise walking path from start to end."""
        if start not in self.graph or end not in self.graph:
            return None, float('infinity')

        distances, previous_nodes = self.dijkstra(start)
        
        if distances[end] == float('infinity'):
            return None, float('infinity') # No path exists
            
        path = []
        current = end
        while current:
            path.append(current)
            current = previous_nodes[current]
            
        path.reverse()
        return path, distances[end]

    def optimize_pick_route(self, start_point: str, pick_list: list):
        """
        Approximates the Traveling Salesperson Problem (TSP) using Nearest Neighbor.
        Finds a highly efficient walking route to grab all items in the pick_list.
        """
        valid_picks = [p for p in pick_list if p in self.graph]
        if not valid_picks:
            return [start_point], 0

        route = [start_point]
        total_distance = 0
        current_location = start_point
        remaining_picks = set(valid_picks)
        
        while remaining_picks:
            distances, _ = self.dijkstra(current_location)
            
            # Find the closest unpicked item from our current location
            closest_item = min(remaining_picks, key=lambda item: distances[item])
            
            route.append(closest_item)
            total_distance += distances[closest_item]
            current_location = closest_item
            remaining_picks.remove(closest_item)
            
        return route, total_distance

# Quick test block to verify graph logic
if __name__ == "__main__":
    warehouse = WarehouseGraph()
    
    # Building a miniature warehouse layout (Nodes = Aisles/Zones, Edges = Distance in meters)
    print("Building warehouse map...")
    warehouse.add_path("Entrance", "A-1", 10)
    warehouse.add_path("Entrance", "B-1", 15)
    warehouse.add_path("A-1", "A-2", 5)
    warehouse.add_path("A-1", "B-1", 8)
    warehouse.add_path("B-1", "B-2", 5)
    warehouse.add_path("A-2", "C-1", 12)
    warehouse.add_path("B-2", "C-1", 6)
    
    print("\nCalculating shortest path from Entrance to C-1...")
    path, dist = warehouse.get_shortest_path("Entrance", "C-1")
    print(f"Path: {' -> '.join(path)} | Total Distance: {dist}m")
    
    print("\nGenerating optimized Pick Route for items in A-2, B-1, and C-1...")
    items_to_pick = ["C-1", "A-2", "B-1"]
    route, total_dist = warehouse.optimize_pick_route("Entrance", items_to_pick)
    print(f"Optimized Walking Route: {' -> '.join(route)}")
    print(f"Total Walking Distance: {total_dist}m")