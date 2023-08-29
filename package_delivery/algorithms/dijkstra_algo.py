import heapq
import math


# src-> Hub to start all deliveries from
# min_heap as priority queue to find minimum-distance neighbor, greedy approach: find min_distance
# visited_queue = [] node after find minimum-distance neighbor
# find a path to from start_vertex to end_vertex pred_vertex, whenever comparison to assign distance, append pred_vertex
#
def dijkstra(graph1, src, route):
    """
    Calculates the shortest distances and predecessor vertices for a given source vertex in a weighted graph using
    Dijkstra's algorithm.

    Parameters:
    - graph1 (Graph): The graph object representing the weighted graph.
    - src (int): The source vertex from which to calculate the shortest distances.
    - route (list): The list of vertices to consider in the calculation of shortest distances.

    Returns: - distances (dict): A dictionary mapping each vertex in the route to its shortest distance from the
    source vertex. - pred_vertex (dict): A dictionary mapping each vertex in the graph to its predecessor vertex in
    the shortest path from the source vertex.
    """
    distances: dict = {node: math.inf for node in route}  # Initialize all distances to infinity in route
    pred_vertex: dict = {node: None for node in graph1.get_vertices}  # Initialize predecessor vertices to None
    distances[src] = 0  # Set source vertex distance to 0
    # The min-heap is used to prioritize processing vertices with the shortest known distance first,
    # ensuring that we find the shortest paths efficiently during the Dijkstra's algorithm execution.
    min_heap = [(0, src)]  # Create a min-heap queue of (distance, vertex) tuples

    visited_queue = []  # Track visited vertices

    # Continue the loop until the min_heap is not empty.
    # The min_heap will be empty when all vertices have been visited and processed.
    while min_heap:
        # Pop the vertex with the smallest distance from the min_heap.
        # Will be src vertex initially
        # The heapq.heappop() function automatically selects the vertex with the smallest distance
        # due to the use of a min-heap.
        current_distance, current_vertex = heapq.heappop(min_heap)
        # Skip if already in visited_queue and current_distance is currently stored distance
        if current_vertex in visited_queue and current_distance > distances[current_vertex]:
            continue
        visited_queue.append(current_vertex)  # Mark the vertex as visited

        # Check if neighbor is in route before entering the loop
        neighbors = [neighbor for neighbor in graph1.get_edge_weight[current_vertex].keys() if neighbor in route]
        # Iterate over the neighbors of the current_vertex and their corresponding weights
        for neighbor in neighbors:
            weight = graph1.get_edge_weight[current_vertex][neighbor]
            # Calculate the total distance to the neighbor by adding the weight of the edge
            # between the current_vertex and the neighbor to the distance of the current_vertex.
            total_distance = current_distance + weight
            # If the calculated distance is smaller than the current known distance to the neighbor,
            # update the distances dictionary with the new, smaller distance.
            if total_distance < distances[neighbor]:
                distances[neighbor] = total_distance
                # Update the predecessor vertex for the 'neighbor' vertex to be the 'current_vertex'.
                pred_vertex[neighbor] = current_vertex
                # Push the updated distance and 'neighbor' vertex as a tuple into the min-heap.
                # This ensures that the 'neighbor' vertex will be processed later with its updated distance.
                heapq.heappush(min_heap, (total_distance, neighbor))
    # Returns distances and pred_vertex dictionaries
    return distances, pred_vertex


def print_distances_and_pred_vertex(distances, pred_vertex):
    """
    Print the distances and predecessor vertices.

    Parameters:
        distances (dict): A dictionary containing the distances of each vertex.
        pred_vertex (dict): A dictionary containing the predecessor vertex of each vertex.

    Returns:
        None
    """
    print("Distances:")
    for vertex, distance in distances.items():
        print(f"{vertex}: {distance}")

    print("\nPredecessor Vertices:")
    for vertex, predecessor in pred_vertex.items():
        print(f"{vertex}: {predecessor}")
